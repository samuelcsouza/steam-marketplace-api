from fastapi import APIRouter, Query, Depends

from src.dependencies import get_service
from src.services.steam import SteamService
from src.config.settings import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/{appid}")
async def get_marketplace_data(
    appid: int,
    item: str = Query(None),
    fill: bool = Query(True),
    steam_service=Depends(get_service(SteamService))
):
    result = steam_service.get_item_marketplace_values(appid, item, fill)

    return result
