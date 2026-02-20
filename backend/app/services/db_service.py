from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models.market import MarketData, Ticker
from app.schemas.market import MarketDataSchema
from core.gemini_logger import logger
import pandas as pd
import os
from urllib.parse import urlsplit, urlunsplit

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/marketflow"
)
# Force asyncpg driver if not present
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


def _mask_database_url(url: str) -> str:
    try:
        parts = urlsplit(url)
        if not parts.netloc:
            return "***"

        netloc = parts.netloc
        if "@" in netloc:
            credentials, host = netloc.rsplit("@", 1)
            user = credentials.split(":", 1)[0] if credentials else ""
            masked_user = f"{user[:2]}***" if user else "***"
            netloc = f"{masked_user}:***@{host}"

        return urlunsplit((parts.scheme, netloc, parts.path, "", ""))
    except Exception:
        return "***"


logger.log(
    "system",
    f"Initializing DB engine with DATABASE_URL={_mask_database_url(DATABASE_URL)}",
    "db_service",
)
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class DBService:
    async def save_tickers(self, tickers: list[str]):
        """
        Ensures tickers exist in the DB to satisfy FK constraints.
        """
        async with AsyncSessionLocal() as session:
            for symbol in tickers:
                # Naive upsert: Check if exists, if not create.
                # Ideally use ON CONFLICT DO NOTHING.
                existing = await session.get(Ticker, symbol)
                if not existing:
                    # For now just symbol and is_etf guess
                    is_etf = symbol.startswith("XL") or symbol == "IYR"
                    record = Ticker(symbol=symbol, is_etf=is_etf)
                    session.add(record)

            await session.commit()
            logger.log("system", f"Ensured {len(tickers)} tickers exist", "db_save")

    async def save_market_data(self, data: pd.DataFrame):
        """
        Saves multi-index DataFrame from yfinance group_by='ticker' to DB.
        """
        async with AsyncSessionLocal() as session:
            # Check structure: if multi-index (Ticker, Ohlcv), iterate tickers
            if isinstance(data.columns, pd.MultiIndex):
                tickers = data.columns.levels[0]
                for symbol in tickers:
                    df_ticker = data[symbol].copy()
                    await self._process_single_ticker(session, symbol, df_ticker)
            else:
                # Single ticker likely passed, or flattened.
                # Ideally fetcher returns consistent structure.
                # For now assume multi-index from fetcher batch.
                pass

            await session.commit()

    async def _process_single_ticker(
        self, session: AsyncSession, symbol: str, df: pd.DataFrame
    ):
        df = df.dropna()
        records = []
        for index, row in df.iterrows():
            try:
                # Validate with Pydantic
                schema = MarketDataSchema(
                    symbol=symbol,
                    date=index,
                    open=row["Open"],
                    high=row["High"],
                    low=row["Low"],
                    close=row["Close"],
                    volume=row["Volume"],
                )

                # Create Model
                record = MarketData(
                    time=schema.date,
                    symbol=schema.symbol,
                    open=schema.open,
                    high=schema.high,
                    low=schema.low,
                    close=schema.close,
                    volume=schema.volume,
                )
                records.append(record)
            except Exception as e:
                logger.log(
                    "system",
                    f"Validation Error for {symbol} at {index}: {e}",
                    "db_save",
                )

        if records:
            # Bulk insert logic or merge?
            # TimescaleDB hypertable handles inserts well.
            # For overwrite, we might need upsert.
            # Simple add_all for now.
            session.add_all(records)
            logger.log("system", f"Saved {len(records)} rows for {symbol}", "db_save")


db_service = DBService()
