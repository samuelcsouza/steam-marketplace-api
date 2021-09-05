from src.services.crawler import Crawler
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/marketplace")
async def get_marketplace_data(
    skin = Query(None),
    interval = Query(None)
):

    fields = {
        'skin': skin,
        'interval': interval
    }

    try:
        result = await Crawler.get_marketplace_data(fields)
    except Exception as exc:
        return {'Error!': str(exc)}

    return result
