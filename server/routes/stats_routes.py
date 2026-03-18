from fastapi import APIRouter
from server.database import stats_collection, page_stats_collection

router = APIRouter()


@router.get("/stats")
async def get_stats(period: str):

    stats = []

    cursor = stats_collection.find({"period": period})

    async for s in cursor:
        s["_id"] = str(s["_id"])
        stats.append(s)

    return stats


@router.get("/page-stats")
async def get_page_stats():

    pages = []

    cursor = page_stats_collection.find()

    async for p in cursor:
        p["_id"] = str(p["_id"])
        pages.append(p)

    return pages