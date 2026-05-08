from fastapi import APIRouter, Depends
from server.schemas.timeline_schema import TimelineCreate, TimelineUpdate
from server.auth import get_admin_user
from server.controllers.timeline_controller import (
    create_timeline_controller,
    get_timeline_controller,
    update_timeline_controller,
    delete_timeline_controller,
    get_all_timelines_controller
)

router = APIRouter(prefix="/timeline", tags=["Timeline"])

@router.post("", dependencies=[Depends(get_admin_user)])
async def create_timeline(timeline: TimelineCreate):
    return await create_timeline_controller(timeline)

@router.get("")
async def get_all_timelines():
    return await get_all_timelines_controller()

@router.get("/{time_id}")
async def get_timeline(time_id: str):
    return await get_timeline_controller(time_id)

@router.put("/{time_id}", dependencies=[Depends(get_admin_user)])
async def update_timeline(time_id: str, data: TimelineUpdate):
    return await update_timeline_controller(time_id, data)

@router.delete("/{time_id}", dependencies=[Depends(get_admin_user)])
async def delete_timeline(time_id: str):
    return await delete_timeline_controller(time_id)
