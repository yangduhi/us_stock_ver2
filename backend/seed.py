import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.fetcher import fetcher
from app.services.db_service import db_service
from core.gemini_logger import logger
from init_db import init_db

TARGET_TICKERS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "NVDA",
    "TSLA",
    "META",
    "BRK-B",
    "JNJ",
    "V",  # Top 10
    "XLK",
    "XLF",
    "XLV",
    "XLE",
    "XLY",
    "XLI",
    "XLC",
    "XLU",
    "XLP",
    "XLB",
    "IYR",  # Sectors
]


async def seed_data():
    print("🌱 Starting Seed Process...")
    logger.log("system", "Starting Seed Process", "seed")

    # 0. Initialize DB Tables
    print("Initializing DB Tables...")
    await init_db()

    # 1. Fetch Data
    print(f"Fetching data for {len(TARGET_TICKERS)} tickers...")
    try:
        data = await fetcher.fetch_batch_history(
            TARGET_TICKERS, period="1mo"
        )  # 1 month for quick seed
        print("Data fetched. Saving to DB...")

        # 1.5 Ensure Tickers Exist (FK Constraint)
        print("Ensuring Tickers exist in DB...")
        await db_service.save_tickers(TARGET_TICKERS)

        # 2. Save Data
        await db_service.save_market_data(data)
        print("✅ Seed Complete!")
        logger.log("system", "Seed Complete", "seed")

    except Exception as e:
        print(f"❌ Seed Failed: {e}")
        logger.log("system", f"Seed Failed: {e}", "seed")


if __name__ == "__main__":
    asyncio.run(seed_data())
