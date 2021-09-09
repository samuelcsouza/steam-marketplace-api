from src.services.crawler import Crawler
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/")
async def get_marketplace_data(
    item = Query(None),
    interval = Query(None)
):

    fields = {
        'item': item,
        'interval': interval
    }

    try:
        result = await Crawler.get_marketplace_data(fields)
    except Exception as exc:
        return {'Error!': str(exc)}

    return result
