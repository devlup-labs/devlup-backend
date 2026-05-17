from fastapi import APIRouter
from typing import List
from server.projects_website.schemas.stats_schema import StatCreate
from server.projects_website.models.stats_model import StatModel
import server.projects_website.controllers.stats_controller as stat_controller

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.post("/visit", response_model=StatModel)
async def record_visit(stat: StatCreate):
    return await stat_controller.record_new_visit(stat)

@router.get("/visits", response_model=List[StatModel])
async def get_visits():
    return await stat_controller.get_all_visits()
