from fastapi import APIRouter
from app.api.endpoints import market, news, dashboard
# from app.api.endpoints import auth # Future

api_router = APIRouter()

api_router.include_router(market.router, prefix="/market", tags=["Market Data"])
api_router.include_router(news.router, prefix="/news", tags=["News & Earnings"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard Aggregation"])
