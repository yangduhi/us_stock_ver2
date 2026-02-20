from fastapi import APIRouter
from app.services.news_service import news_service

router = APIRouter()


@router.get("/general")
async def get_general_news(category: str = "general"):
    return await news_service.get_market_news(category)


@router.get("/earnings")
async def get_earnings_calendar():
    return await news_service.get_earnings_calendar()
