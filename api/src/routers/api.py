from fastapi import APIRouter
from .endpoints import market_data

api_router = APIRouter()

api_router.include_router(market_data.router, prefix="/730", tags=["csgo"])
