import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def debug_db():
    db_url = os.getenv("DATABASE_URL", "Not Set")
    print(f"DEBUG: DATABASE_URL is '{db_url}'")

    if not db_url.startswith("postgresql+asyncpg://"):
        print(
            "WARNING: Scheme is not postgresql+asyncpg. Fixing manually for this test."
        )
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

    try:
        engine = create_async_engine(db_url)
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version();"))
            val = result.scalar()
            print(f"SUCCESS: Connected to DB. Version: {val}")

            res_count = await conn.execute(text("SELECT count(*) FROM market_data;"))
            count = res_count.scalar()
            print(f"SUCCESS: market_data count is {count}")
    except Exception as e:
        print(f"FAILURE: DB Connection failed: {e}")
    finally:
        try:
            os.remove(__file__)
        except OSError:
            pass


if __name__ == "__main__":
    asyncio.run(debug_db())
