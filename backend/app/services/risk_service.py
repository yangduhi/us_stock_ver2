import yfinance as yf
import pandas as pd
import numpy as np
from core.gemini_logger import logger
from app.core.cache import cache
import asyncio


class RiskService:
    async def analyze_risk(self, tickers: list):
        if not tickers:
            return {"volatility": 0, "matrix": {}, "high_correlations": []}

        tickers_key = ",".join(sorted(tickers))
        cache_key = f"risk:analysis:{tickers_key}"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self._calculate_risk, tickers)
            await cache.set(cache_key, result, expire=3600 * 4)  # 4 hours
            return result
        except Exception as e:
            logger.log("error", f"Risk analysis failed: {str(e)}", "risk_service")
            return {
                "volatility": 0,
                "matrix": {},
                "high_correlations": [],
                "error": str(e),
            }

    def _calculate_risk(self, tickers):
        try:
            # Download data
            data = yf.download(tickers, period="6mo", progress=False)["Close"]

            if data.empty:
                return {"volatility": 0, "matrix": {}, "high_correlations": []}

            # If single ticker, it returns Series, need DataFrame
            if isinstance(data, pd.Series):
                data = data.to_frame()

            returns = data.pct_change().dropna()

            if returns.empty:
                return {"volatility": 0, "matrix": {}, "high_correlations": []}

            # Correlation Matrix
            corr = returns.corr()
            high_corr = []
            cols = corr.columns

            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    val = corr.iloc[i, j]
                    if val > 0.8:
                        high_corr.append(
                            {
                                "asset1": str(cols[i]),
                                "asset2": str(cols[j]),
                                "correlation": round(float(val), 2),
                            }
                        )

            # Volatility (Annualized)
            cov = returns.cov() * 252
            weights = np.array([1 / len(cols)] * len(cols))

            try:
                var = np.dot(weights.T, np.dot(cov, weights))
                vol = np.sqrt(var)
            except:
                vol = 0

            # Convert matrix to list of lists for frontend heatmap
            # Or just dict for now
            # We'll stick to a simple structure: nodes and links?
            # or just the matrix as dict keys

            matrix_dict = {}
            for c1 in cols:
                matrix_dict[str(c1)] = {}
                for c2 in cols:
                    matrix_dict[str(c1)][str(c2)] = round(float(corr.loc[c1, c2]), 2)

            return {
                "volatility": round(float(vol) * 100, 2),
                "high_correlations": high_corr,
                "matrix": matrix_dict,
                "tickers": [str(x) for x in cols],
            }

        except Exception as e:
            logger.log("error", f"Risk calc internal error: {str(e)}", "risk_service")
            raise e


risk_service = RiskService()
