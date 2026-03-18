from fastapi import APIRouter
from bson import ObjectId
from datetime import datetime
from server.database import project_collection
from server.schemas.project_schema import Project

router = APIRouter()


# ----------------------------------------------------
# GET /projects
# GET /projects?status=ongoing
# GET /projects?has_issues=true
# GET /projects?type=woc
# GET /projects?year=2025
# ----------------------------------------------------

@router.get("/projects")
async def get_projects(
    status: str | None = None,
    has_issues: bool | None = None,
    type: str | None = None,
    year: int | None = None
):

    query = {}

    if status:
        query["status"] = status

    if has_issues is not None:
        query["has_issues"] = has_issues

    if type:
        query["type"] = type

    if year:
        query["year"] = year

    projects = []

    cursor = project_collection.find(query)

    async for project in cursor:
        project["_id"] = str(project["_id"])
        projects.append(project)

    return projects


# ----------------------------------------------------
# POST /projects
# ----------------------------------------------------

@router.post("/projects")
async def create_project(project: Project):

    project_data = project.dict()

    project_data["created_at"] = datetime.utcnow()
    project_data["updated_at"] = datetime.utcnow()

    result = await project_collection.insert_one(project_data)

    return {
        "project_id": str(result.inserted_id)
    }


# ----------------------------------------------------
# GET /projects/{project_id}
# ----------------------------------------------------

@router.get("/projects/{project_id}")
async def get_project(project_id: str):

    project = await project_collection.find_one(
        {"_id": ObjectId(project_id)}
    )

    if project:
        project["_id"] = str(project["_id"])

    return project


# ----------------------------------------------------
# PUT /projects/{project_id}
# ----------------------------------------------------

@router.put("/projects/{project_id}")
async def update_project(project_id: str, data: dict):

    data["updated_at"] = datetime.utcnow()

    await project_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": data}
    )

    return {"message": "Project updated"}


# ----------------------------------------------------
# DELETE /projects/{project_id}
# ----------------------------------------------------

@router.delete("/projects/{project_id}")
async def delete_project(project_id: str):

    await project_collection.delete_one(
        {"_id": ObjectId(project_id)}
    )

    return {"message": "Project deleted"}