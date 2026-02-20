import asyncio
import httpx
import logging
import time

# Configure Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("scheduler")

API_URL = "http://backend:8000/api/v1"


async def warm_cache():
    """
    Periodically fetches dashboard data to keep cache warm.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            try:
                logger.info("Warming Dashboard Cache...")
                resp = await client.get(f"{API_URL}/dashboard/overview")
                if resp.status_code == 200:
                    logger.info("Dashboard Cache Warmed successfully.")
                else:
                    logger.error(f"Failed to warm dashboard: {resp.status_code}")

                # Fetch Top Tickers to warm their history/analysis
                # For demo, just wait

            except Exception as e:
                logger.error(f"Scheduler Error: {e}")

            # Wait 60 seconds (Short Cache TTL)
            await asyncio.sleep(60)


if __name__ == "__main__":
    logger.info("Starting Scheduler Service...")
    # Add delay to let backend start
    time.sleep(10)
    asyncio.run(warm_cache())
