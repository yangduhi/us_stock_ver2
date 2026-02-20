import pytz
from datetime import datetime
import yfinance as yf
from app.core.cache import cache
from core.gemini_logger import logger


class MarketService:
    def __init__(self):
        self.tz = pytz.timezone("US/Eastern")

    def get_market_status(self) -> str:
        """
        Returns 'Open' or 'Closed' based on US Market hours.
        """
        now = datetime.now(self.tz)
        # Weekends
        if now.weekday() >= 5:
            return "Closed"

        # 9:30 AM - 4:00 PM
        start = now.replace(hour=9, minute=30, second=0, microsecond=0)
        end = now.replace(hour=16, minute=0, second=0, microsecond=0)

        if start <= now <= end:
            return "Open"
        return "Closed"

    async def get_fear_greed_index(self):
        """
        Fetches the official CNN Fear & Greed Index via CNN's data API.
        This is the most accurate and stable method.
        """
        cache_key = "market:sentiment"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        try:
            import httpx
            # CNN's internal API for Fear & Greed
            url = "https://production.dataviz.cnn.io/index/feargreed/static/daily"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    value = float(data.get("fear_and_greed", {}).get("score", 50))
                    label = data.get("fear_and_greed", {}).get("rating", "Neutral").title()
                    
                    result = {"value": round(value, 1), "label": label}
                    await cache.set(cache_key, result, expire=3600)
                    return result
            
            # Fallback to scraper if API is down
            return await self._get_fallback_scraper()

        except Exception as e:
            logger.log("error", f"CNN API fetch failed: {str(e)}", "market_service")
            return await self.get_fear_greed_proxy()

    async def _get_fallback_scraper(self):
        # Implementation of simple scraper as secondary fallback
        try:
            import httpx
            from bs4 import BeautifulSoup
            import re
            url = "https://www.cnn.com/markets/fear-and-greed"
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(url)
                soup = BeautifulSoup(r.text, "html.parser")
                # CNN often lists the score in meta tags or specific spans
                score_tag = soup.find("span", string=re.compile(r"Fear & Greed Index"))
                if score_tag:
                    val = re.search(r"(\d+)", score_tag.parent.get_text())
                    if val:
                        v = float(val.group(1))
                        return {"value": v, "label": self._get_label_from_value(v)}
            return await self.get_fear_greed_proxy()
        except:
            return await self.get_fear_greed_proxy()

    async def get_composite_sentiment(self, fetcher):
        """
        Calculates a proprietary sentiment score based on Broad Market ETF flows.
        Logic from D:/vscode/US_stock/src/analysis/etf_flow_analyzer.py
        """
        cache_key = "market:composite_sentiment"
        try:
            cached = await cache.get(cache_key)
            if cached:
                return cached
        except Exception:
            pass

        try:
            indices = ["SPY", "QQQ", "IWM"]
            scores = []
            
            for ticker in indices:
                # Fetch recent data (5 days to match previous project logic)
                df = await fetcher.fetch_stock_data(ticker, period="5d")
                if df is None or df.empty or len(df) < 2:
                    logger.log("warn", f"Insufficient data for sentiment calculation: {ticker}", "market_service")
                    continue
                
                # 1. Price Change % (Current vs Previous)
                curr_price = float(df["Close"].iloc[-1])
                prev_price = float(df["Close"].iloc[-2])
                change_pct = (curr_price - prev_price) / prev_price
                
                # 2. Volume Ratio (Current / Average of last 5 days)
                avg_vol = df["Volume"].mean()
                curr_vol = df["Volume"].iloc[-1]
                vol_ratio = curr_vol / avg_vol if avg_vol > 0 else 1.0
                
                # 3. Flow Score (Original formula: change_pct * 100 * vol_ratio * 10)
                # This gives a value roughly between -100 and 100.
                # Neutral (0) should map to 50 in our 0-100 scale.
                flow_score = change_pct * 100 * vol_ratio * 10
                
                # Map to 0-100 scale: score_0_100 = 50 + flow_score
                # Example: 0.2% change, 1.2 vol ratio -> 0.2 * 1.2 * 10 = 2.4 -> 52.4
                mapped_score = 50 + flow_score
                scores.append(mapped_score)
            
            if not scores:
                return {"value": 50.0, "label": "Neutral"}
                
            value = round(sum(scores) / len(scores), 1)
            value = max(0.0, min(100.0, value))
            
            result = {"value": value, "label": self._get_label_from_value(value)}
            try:
                await cache.set(cache_key, result, expire=600)
            except Exception:
                pass
            return result
        except Exception as e:
            logger.log("error", f"Composite sentiment critical failure: {str(e)}", "market_service")
            return {"value": 50.0, "label": "Neutral"}

    async def get_fear_greed_proxy(self):
        # Improved proxy based on VIX - more conservative alignment
        try:
            vix = yf.Ticker("^VIX")
            hist = vix.history(period="1d")
            if hist.empty:
                return {"value": 50, "label": "Neutral"}

            vix_price = float(hist["Close"].iloc[-1])
            
            # CNN Greed is usually higher when VIX is lower.
            # 20 is a historical average (Neutral ~50)
            # 15 VIX -> ~65 Greed
            # 25 VIX -> ~35 Fear
            value = 100 - (vix_price * 2.5) # 20 * 2.5 = 50
            value = max(0, min(100, round(value, 1)))
            
            return {"value": value, "label": self._get_label_from_value(value)}
        except Exception:
            return {"value": 50, "label": "Neutral"}


market_service = MarketService()
