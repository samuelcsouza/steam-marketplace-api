from fastapi import APIRouter, Query
from src.services.external.steam import SteamService
from src.config.settings import get_settings

router = APIRouter()
settings = get_settings()

steam_service = SteamService(
    steam_url_marketplace=settings.STEAM_MARKETPLACE_URL
)


@router.get("/{appid}")
async def get_marketplace_data(
    appid: int,
    item: str = Query(None),
    fill: bool = Query(True)
):
    result = steam_service.get_item_marketplace_values(appid, item, fill)

    return result
