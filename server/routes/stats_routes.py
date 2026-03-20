from fastapi import APIRouter, Query
from server.database import stats_collection, page_stats_collection

router = APIRouter()


# GET /stats?period=week/month/year
@router.get("/stats")
async def get_stats(period: str = Query(None)):
    
    query = {}

    # filter by period if provided
    if period:
        if period not in ["week", "month", "year"]:
            return {"error": "Invalid period. Use week/month/year"}
        query["period"] = period

    stats = await stats_collection.find(query).to_list(100)

    return {
        "count": len(stats),
        "data": stats
    }


# GET /page-stats
@router.get("/page-stats")
async def get_page_stats(period: str = Query(None)):

    query = {}

    if period:
        if period not in ["week", "month", "year"]:
            return {"error": "Invalid period"}
        query["period"] = period

    stats = await page_stats_collection.find(query).to_list(100)

    return {
        "count": len(stats),
        "data": stats
    }