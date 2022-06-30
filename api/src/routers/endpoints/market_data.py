from fastapi import APIRouter, Query, HTTPException
from src.services.external.steam import SteamService

router = APIRouter()

steam_service = SteamService(
    steam_url_marketplace="https://steamcommunity.com/market/listings/730/"
)


@router.get("/")
async def get_marketplace_data(
    item=Query(None)
):

    try:
        result = steam_service.get_item_marketplace_values(item)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    return result
