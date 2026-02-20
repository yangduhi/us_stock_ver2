from fastapi import APIRouter
from app.services.fetcher import fetcher
from app.services.ai_service import ai_service
from app.core.cache import cache
from app.services.market_service import market_service
import asyncio

router = APIRouter()


@router.get("/overview")
async def get_dashboard_overview():
    """
    BFF Endpoint: Aggregates Indices, Sector Performance, and Fear & Greed.
    Optimized for Dashboard 'Above the Fold' view.
    Target Latency: < 200ms (Cached)
    """
    cache_key = "dashboard:overview"
    cached = await cache.get(cache_key)
    if cached:
        return cached

    try:
        # Define tasks
        async def get_index_change(f, s):
            try:
                df = await f.fetch_stock_data(s, period="2d")
                if df.empty or len(df) < 2:
                    return {s: 0.0}
                change = (
                    (df["Close"].iloc[-1] - df["Close"].iloc[-2]) / df["Close"].iloc[-2]
                ) * 100
                return {s: round(change, 2)}
            except Exception as e:
                print(f"Error fetching {s}: {e}")
                return {s: 0.0}

        indices = ["SPY", "QQQ", "IWM"]
        sectors = ["XLK", "XLE", "XLF", "XLV"]

        # Run all fetches concurrently
        results = await asyncio.gather(
            *[get_index_change(fetcher, ticker) for ticker in indices + sectors],
            market_service.get_fear_greed_index(),
            market_service.get_composite_sentiment(fetcher),
        )

        # Result mapping
        composite_sentiment = results[-1]
        official_fear_greed = results[-2]
        market_results = results[:-2]

        # Process Results
        market_data = {}
        for res in market_results:
            market_data.update(res)

        # Construct Response
        response = {
            "indices": {k: v for k, v in market_data.items() if k in indices},
            "sectors": {k: v for k, v in market_data.items() if k in sectors},
            "market_status": market_service.get_market_status(),
            "fear_greed": official_fear_greed,
            "market_sentiment": composite_sentiment, # New Gauge Value
        }

        await cache.set(cache_key, response, expire=60)
        return response

    except Exception as e:
        return {"error": str(e), "indices": {}, "sectors": {}}


@router.get("/ai-intelligence")
async def get_ai_intelligence():
    """
    Get AI-generated market intelligence summary.
    """
    cache_key = "dashboard:ai_intelligence"
    cached = await cache.get(cache_key)
    if cached:
        return cached

    ticker = "SPY"
    try:
        df = await fetcher.fetch_stock_data(ticker, period="2d")
        change = 0.0
        if not df.empty and len(df) >= 2:
            change = (
                (df["Close"].iloc[-1] - df["Close"].iloc[-2]) / df["Close"].iloc[-2]
            ) * 100

        # Run blockable sync AI code in thread
        analysis = await asyncio.to_thread(ai_service.analyze_news, ticker, change)
        await cache.set(cache_key, analysis, expire=300)
        return analysis
    except Exception as e:
        return {"error": str(e), "summary": "AI Intelligence currently unavailable."}
