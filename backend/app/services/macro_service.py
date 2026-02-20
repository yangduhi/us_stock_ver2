import os
from fredapi import Fred
from core.gemini_logger import logger
from app.core.cache import cache


class MacroService:
    def __init__(self):
        self.api_key = os.getenv("FRED_API_KEY")
        if not self.api_key:
            logger.log("warning", "FRED_API_KEY not found", "macro_service")
            self.fred = None
        else:
            self.fred = Fred(api_key=self.api_key)

    async def get_economic_indicators(self):
        """
        Fetches key economic indicators:
        - CPI (Inflation)
        - GDP
        - Unemployment Rate
        - 10Y-2Y Treasury Yield Spread
        - M2 Money Supply
        """
        if not self.fred:
            return {"error": "FRED API key missing"}

        cache_key = "macro:indicators"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        try:
            # Series IDs
            series_ids = {
                "CPI": "CPIAUCSL",
                "GDP": "GDP",
                "Unemployment": "UNRATE",
                "10Y_Yield": "DGS10",
                "2Y_Yield": "DGS2",
                "M2": "M2SL",
            }

            data = {}
            for name, series_id in series_ids.items():
                try:
                    series = self.fred.get_series(series_id, limit=1)
                    if not series.empty:
                        data[name] = {
                            "value": float(series.iloc[-1]),
                            "date": series.index[-1].strftime("%Y-%m-%d"),
                        }
                except Exception as e:
                    logger.log(
                        "error", f"Failed to fetch {name}: {str(e)}", "macro_service"
                    )

            # Calculate Yield Curve Inversion
            if "10Y_Yield" in data and "2Y_Yield" in data:
                spread = data["10Y_Yield"]["value"] - data["2Y_Yield"]["value"]
                data["Yield_Spread_10Y_2Y"] = {
                    "value": spread,
                    "date": data["10Y_Yield"]["date"],
                    "status": "Inverted" if spread < 0 else "Normal",
                }

            await cache.set(cache_key, data, expire=86400)  # Cache for 24 hours
            return data

        except Exception as e:
            logger.log("error", f"Macro fetch failed: {str(e)}", "macro_service")
            return {"error": str(e)}


macro_service = MacroService()
