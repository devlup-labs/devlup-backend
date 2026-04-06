from fastapi import APIRouter, Query
from server.controllers.stats_controller import (
    get_stats_controller,
    get_page_stats_controller
)

router = APIRouter()


@router.get("/stats")
async def get_stats(period: str = Query(None)):
    return await get_stats_controller(period)


@router.get("/page-stats")
async def get_page_stats(period: str = Query(None)):
    return await get_page_stats_controller(period)