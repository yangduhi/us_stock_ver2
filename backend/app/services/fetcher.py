import yfinance as yf
import pandas as pd
import asyncio
from typing import List
import random
from core.gemini_logger import logger


# Decorator for Exponential Backoff
def retry_with_backoff(retries=3, delay=1, backoff=2):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            current_delay = delay
            for i in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logger.log(
                        "system", f"Attempt {i + 1} failed: {str(e)}", "fetcher_retry"
                    )
                    if i == retries - 1:
                        raise e
                    sleep_time = current_delay + random.uniform(0, 1)  # Add jitter
                    await asyncio.sleep(sleep_time)
                    current_delay *= backoff

        return wrapper

    return decorator


class DataFetcher:
    def __init__(self):
        self._semaphore = None

    @property
    def semaphore(self):
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(5)
        return self._semaphore

    @retry_with_backoff(retries=5, delay=2)
    async def fetch_batch_history(
        self, tickers: List[str], period="1y"
    ) -> pd.DataFrame:
        if not tickers:
            return pd.DataFrame()

        async with self.semaphore:
            # yfinance download is blocking, run in executor
            loop = asyncio.get_event_loop()

            def match_download():
                # group_by='ticker' ensures multi-index if multiple tickers
                # yfinance can hang, so we use a thread-safe-ish way or just trust timeout
                return yf.download(
                    tickers,
                    period=period,
                    group_by="ticker",
                    threads=True,
                    progress=False,
                    timeout=15,  # 15s timeout
                )

            data = await loop.run_in_executor(None, match_download)
            return data

    async def fetch_stock_data(self, ticker: str, period="1y") -> pd.DataFrame:
        """
        Fetches historical data for a single ticker.
        Wraps fetch_batch_history for convenience.
        """
        df = await self.fetch_batch_history([ticker], period=period)
        if df.empty:
            return pd.DataFrame()

        # Handle MultiIndex if present (yfinance downloads with group_by='ticker' often return MultiIndex)
        # But if we pass single ticker to yf.download, it might not be multi-index depending on version.
        # Our fetch_batch_history uses group_by='ticker', so it will be MultiIndex (Ticker, Level).

        if isinstance(df.columns, pd.MultiIndex):
            try:
                # Check levels: If Ticker is in level 0
                if ticker in df.columns.get_level_values(0):
                    return df.xs(ticker, level=0, axis=1)
                elif ticker.upper() in df.columns.get_level_values(0):
                    return df.xs(ticker.upper(), level=0, axis=1)

                # If unique level 0 values check out (e.g. only 1 ticker but name mismatch?)
                unique_tickers = df.columns.get_level_values(0).unique()
                if len(unique_tickers) == 1:
                    return df.droplevel(0, axis=1)

                return df
            except Exception as e:
                logger.log("error", f"Flatten failed: {e}", "fetcher")
                return df
        return df

    async def get_scaler_data(self, ticker: str):
        # Fetch single ticker info/calendar
        pass


fetcher = DataFetcher()
