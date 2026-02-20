from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.market_service import market_service
from app.services.macro_service import macro_service
from app.services.risk_service import risk_service
from app.services.screener_service import screener_service
from app.services.fetcher import fetcher
from app.services.analyzer import quant_analyzer

router = APIRouter()


@router.get("/status")
def get_market_status():
    return {"status": market_service.get_market_status()}


@router.get("/fear-greed")
async def get_fear_greed():
    return await market_service.get_fear_greed_index()


@router.get("/macro")
async def get_macro_data():
    return await macro_service.get_economic_indicators()


@router.get("/risk")
async def get_risk_analysis(tickers: Optional[str] = Query(None)):
    """
    Get risk analysis for a portfolio.
    Tickers should be comma separated. Default: Top Tech checks
    """
    if tickers:
        ticker_list = [t.strip().upper() for t in tickers.split(",")]
    else:
        ticker_list = [
            "AAPL",
            "NVDA",
            "MSFT",
            "GOOGL",
            "AMZN",
            "TSLA",
            "META",
        ]  # Default

    return await risk_service.analyze_risk(ticker_list)


@router.get("/screener/smart-money")
async def get_smart_money_picks(top: int = 20):
    return await screener_service.run_smart_money_screen(top)


@router.get("/tickers/{ticker}/analysis")
async def get_ticker_analysis(ticker: str, period: str = "1y"):
    symbol = ticker.strip().upper()
    if not symbol:
        raise HTTPException(status_code=400, detail="Ticker is required")

    try:
        df = await fetcher.fetch_stock_data(symbol, period=period)
        if df is None or df.empty:
            return {
                "symbol": symbol,
                "date": None,
                "price": 0.0,
                "score": 50,
                "label": "Hold",
                "signals": [],
                "indicators": {"rsi": 50, "sma200": 0, "macd": 0},
                "warning": "No data available; returning fallback analysis.",
            }

        result = quant_analyzer.analyze(df.copy())
        if "error" in result:
            raise ValueError(result["error"])
        result["symbol"] = symbol
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to analyze ticker {symbol}: {e}"
        ) from e
