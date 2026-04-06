from server.database import stats_collection, page_stats_collection

# GET stats
async def get_stats_controller(period: str = None):
    query = {}

    if period:
        if period not in ["week", "month", "year"]:
            return {"error": "Invalid period"}
        query["period"] = period

    stats = await stats_collection.find(query).to_list(100)

    return {
        "count": len(stats),
        "data": stats
    }


# GET page stats
async def get_page_stats_controller(period: str = None):
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