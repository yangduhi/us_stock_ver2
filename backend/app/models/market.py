from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ticker(Base):
    __tablename__ = "tickers"

    symbol = Column(String, primary_key=True, index=True)
    name = Column(String)
    sector = Column(String, index=True)
    industry = Column(String)
    is_etf = Column(Boolean, default=False)

    market_data = relationship("MarketData", back_populates="ticker")


class MarketData(Base):
    __tablename__ = "market_data"

    # Composite PK handled by TimescaleDB usually, but for SQLAlchemy we need a PK or logic
    # We use (symbol, date) as logical PK.

    time = Column(
        DateTime, primary_key=True, nullable=False
    )  # 'time' is standard for Timescale
    symbol = Column(
        String, ForeignKey("tickers.symbol"), primary_key=True, nullable=False
    )

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)  # Float to handle large numbers or fractional crypto

    ticker = relationship("Ticker", back_populates="market_data")


class MacroData(Base):
    __tablename__ = "macro_data"

    series_id = Column(String, primary_key=True)  # e.g., CPIAUCSL
    date = Column(DateTime, primary_key=True)
    value = Column(Float)


class Financials(Base):
    __tablename__ = "financials"

    symbol = Column(String, ForeignKey("tickers.symbol"), primary_key=True, index=True)
    period = Column(DateTime, primary_key=True)  # Report Date
    revenue = Column(Float)
    net_income = Column(Float)
    eps = Column(Float)
    total_debt = Column(Float)
    equity = Column(Float)
    roe = Column(Float)


class MarketSentiment(Base):
    __tablename__ = "market_sentiment"

    date = Column(DateTime, primary_key=True)
    source = Column(String, primary_key=True)  # e.g., 'FearGreed'
    score = Column(Float)  # 0-100


class Holdings(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, ForeignKey("tickers.symbol"), index=True)
    holder = Column(String)
    shares = Column(Float)
    date_reported = Column(DateTime)
    pct_held = Column(Float)
