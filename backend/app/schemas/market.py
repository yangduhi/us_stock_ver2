from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class MarketDataSchema(BaseModel):
    symbol: str
    date: datetime
    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)
    volume: float = Field(ge=0)

    @field_validator("date")
    def validate_date_not_future(cls, v):
        if v > datetime.now():
            # Allow some clock skew but generally future dates are wrong for historical data
            # For real-time, it might be close to now.
            pass
        return v


class TickerSchema(BaseModel):
    symbol: str
    name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    is_etf: bool = False
