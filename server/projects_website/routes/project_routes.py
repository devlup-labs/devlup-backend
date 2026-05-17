from fastapi import APIRouter, HTTPException, Query, status, Depends
from typing import List, Optional

from server.projects_website.auth import get_admin_user
from server.projects_website.schemas.project_schema import ProjectCreate, ProjectUpdate
from server.projects_website.models.project_model import ProjectModel
from server.projects_website.controllers import project_controller

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("", response_model=List[ProjectModel])
async def get_projects(
    status: Optional[str] = Query(None),
    has_issues: Optional[bool] = Query(None),
    type: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    approval_status: Optional[str] = Query(None)
):
    return await project_controller.get_all_projects(status, has_issues, type, year, approval_status)

@router.post("/submit", response_model=ProjectModel, status_code=status.HTTP_201_CREATED)
async def submit_project(project: ProjectCreate):
    return await project_controller.submit_public_project(project)

@router.post("", response_model=ProjectModel, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_admin_user)])
async def create_project(project: ProjectCreate):
    return await project_controller.create_new_project(project)


@router.get("/{project_id}", response_model=ProjectModel, dependencies=[Depends(get_admin_user)])
async def get_project(project_id: str):
    return await project_controller.get_single_project(project_id)


@router.put("/{project_id}", response_model=ProjectModel, dependencies=[Depends(get_admin_user)])
async def update_project(project_id: str, project_update: ProjectUpdate):
    return await project_controller.update_existing_project(project_id, project_update)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_admin_user)])
async def delete_project(project_id: str):
    return await project_controller.delete_existing_project(project_id)