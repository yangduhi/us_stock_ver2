import yfinance as yf
from core.gemini_logger import logger
from app.core.cache import cache
import asyncio


class ScreenerService:
    async def run_smart_money_screen(self, top_n=20):
        cache_key = f"screener:smart_money:{top_n}"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        try:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(None, self._run_screen, top_n)
            await cache.set(cache_key, results, expire=3600 * 12)  # Cache 12 hours
            return results
        except Exception as e:
            logger.log("error", f"Screening failed: {str(e)}", "screener_service")
            return []

    def _run_screen(self, top_n):
        # Default list of candidate tickers (Mega/Large Cap Tech & Fin)
        # In a real app, this would be a wider scan or from DB
        candidates = [
            "AAPL",
            "MSFT",
            "NVDA",
            "GOOGL",
            "AMZN",
            "META",
            "TSLA",
            "JPM",
            "V",
            "MA",
            "WMT",
            "PG",
            "JNJ",
            "XOM",
            "CVX",
            "HD",
            "COST",
            "PEP",
            "KO",
            "AVGO",
            "CSCO",
            "CRM",
            "AMD",
            "INTC",
            "QCOM",
            "TXN",
            "ADBE",
            "NFLX",
            "DIS",
            "NKE",
            "SBUX",
            "MCD",
            "BA",
            "CAT",
            "DE",
            "MMM",
            "GS",
            "MS",
            "BAC",
            "WFC",
            "C",
            "BLK",
            "SPGI",
            "PLTR",
            "SOFI",
            "COIN",
            "MARA",
            "RIOT",
            "DKNG",
        ]

        results = []
        for ticker in candidates:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                hist = stock.history(period="6mo")

                if hist.empty:
                    continue

                # Technical Analysis (Simplified)
                close = hist["Close"]
                ma50 = close.rolling(50).mean().iloc[-1]
                ma200 = close.rolling(200).mean().iloc[-1]
                rsi = self._calculate_rsi(close)

                # Fundamental Analysis
                pe = info.get("trailingPE", 0)

                # Composite Score Logic
                score = 50

                # Trend
                if close.iloc[-1] > ma50:
                    score += 10
                if ma50 > ma200:
                    score += 10  # Golden Cross territory

                # RSI
                if 40 < rsi < 60:
                    score += 5
                elif rsi < 30:
                    score += 15  # Oversold bounce candidate

                # Valuation
                if 0 < pe < 25:
                    score += 10

                # Analyst recommendation
                rec = info.get("recommendationKey", "none")
                if rec in ["buy", "strongBuy"]:
                    score += 10

                results.append(
                    {
                        "ticker": ticker,
                        "name": info.get("shortName", ticker),
                        "sector": info.get("sector", "Unknown"),
                        "price": round(close.iloc[-1], 2),
                        "change": round(
                            (close.iloc[-1] / hist["Close"].iloc[-2] - 1) * 100, 2
                        ),
                        "score": score,
                        "rsi": round(rsi, 1),
                        "pe": round(pe, 2) if pe else "N/A",
                        "recommendation": rec.replace("strong", "Strong ").title(),
                    }
                )

            except Exception:
                continue

        # Sort by score desc
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_n]

    def _calculate_rsi(self, series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs)).iloc[-1]


screener_service = ScreenerService()
