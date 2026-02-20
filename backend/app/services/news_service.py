import os
import finnhub
from core.gemini_logger import logger
from app.core.cache import cache
import asyncio


class NewsService:
    def __init__(self):
        self.api_key = os.getenv("FINNHUB_API_KEY")
        if not self.api_key:
            logger.log("warning", "FINNHUB_API_KEY not found", "news_service")
            self.client = None
        else:
            self.client = finnhub.Client(api_key=self.api_key)

    async def get_market_news(self, category="general"):
        if not self.client:
            return []

        cache_key = f"news:market:{category}"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        try:
            loop = asyncio.get_event_loop()
            news = await loop.run_in_executor(
                None, lambda: self.client.general_news(category, min_id=0)
            )
            # Filter and format
            formatted_news = [
                {
                    "id": item.get("id"),
                    "headline": item.get("headline"),
                    "summary": item.get("summary"),
                    "url": item.get("url"),
                    "image": item.get("image"),
                    "source": item.get("source"),
                    "datetime": item.get("datetime"),
                }
                for item in news[:10]  # Top 10
            ]
            await cache.set(cache_key, formatted_news, expire=1800)  # 30 mins
            return formatted_news
        except Exception as e:
            logger.log("error", f"News fetch failed: {str(e)}", "news_service")
            return []

    async def get_earnings_calendar(self):
        if not self.client:
            return []

        cache_key = "news:earnings_calendar"
        cached = await cache.get(cache_key)
        if cached:
            return cached

        try:
            loop = asyncio.get_event_loop()
            # Get earnings for next 7 days
            import datetime

            start = datetime.date.today()
            end = start + datetime.timedelta(days=7)

            earnings = await loop.run_in_executor(
                None,
                lambda: self.client.earnings_calendar(
                    _from=start.strftime("%Y-%m-%d"),
                    to=end.strftime("%Y-%m-%d"),
                    symbol="",
                    international=False,
                ),
            )

            earnings_list = earnings.get("earningsCalendar", [])
            # Sort by market cap or importance if possible? Finnhub free doesn't give market cap here.
            # We'll just return the list, maybe filtered by important tickers if we had a list.

            await cache.set(cache_key, earnings_list, expire=3600 * 12)  # 12 hours
            return earnings_list
        except Exception as e:
            logger.log("error", f"Earnings fetch failed: {str(e)}", "news_service")
            return []


news_service = NewsService()
