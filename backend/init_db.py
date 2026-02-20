import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.market import Base
from sqlalchemy import text

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/marketflow"
)


async def init_db():
    print("Initializing Database...")
    engine = create_async_engine(DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        # Create Tables
        print("Creating Tables...")
        await conn.run_sync(Base.metadata.create_all)

        # Convert to Hypertable (TimescaleDB specific)
        # We need to execute raw SQL for create_hypertable
        try:
            print("Converting 'market_data' to Hypertable...")
            await conn.execute(
                text(
                    "SELECT create_hypertable('market_data', 'time', if_not_exists => TRUE);"
                )
            )
            print("Hypertable created (or already exists).")
        except Exception as e:
            print(f"Hypertable creation failed (Is TimescaleDB installed?): {e}")

    await engine.dispose()
    print("Database Initialization Complete.")


if __name__ == "__main__":
    asyncio.run(init_db())
