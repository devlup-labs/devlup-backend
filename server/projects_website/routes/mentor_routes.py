from fastapi import APIRouter, Depends
from server.projects_website.schemas.mentor_schema import Mentor
from server.projects_website.auth import get_admin_user
from server.projects_website.controllers.mentor_controller import (
    create_mentor_controller,
    get_mentor_controller,
    update_mentor_controller,
    delete_mentor_controller,
    get_mentors_controller
)

router = APIRouter()

@router.post("/mentors", dependencies=[Depends(get_admin_user)])
async def create_mentor(mentor: Mentor):
    return await create_mentor_controller(mentor)

@router.get("/mentors/{mentor_id}")
async def get_mentor(mentor_id: str):
    return await get_mentor_controller(mentor_id)

@router.put("/mentors/{mentor_id}", dependencies=[Depends(get_admin_user)])
async def update_mentor(mentor_id: str, data: dict):
    return await update_mentor_controller(mentor_id, data)

@router.delete("/mentors/{mentor_id}", dependencies=[Depends(get_admin_user)])
async def delete_mentor(mentor_id: str):
    return await delete_mentor_controller(mentor_id)

@router.get("/mentors")
async def get_mentors(year: int | None = None):
    return await get_mentors_controller(year)