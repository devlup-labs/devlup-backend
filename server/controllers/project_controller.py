from fastapi import HTTPException, status
from typing import List, Optional
from bson import ObjectId
from datetime import datetime, timezone

from server.database import project_collection
from server.schemas.project_schema import ProjectCreate, ProjectUpdate

async def get_all_projects(status: Optional[str] = None, has_issues: Optional[bool] = None, type: Optional[str] = None, year: Optional[int] = None):
    query = {}
    or_conditions = []
    
    if status is not None:
        or_conditions.append({"status": status})
    if has_issues is not None:
        or_conditions.append({"has_issues": has_issues})
    if type is not None:
        or_conditions.append({"type": type})
    if year is not None:
        or_conditions.append({"year": year})
        
    if or_conditions:
        query = {"$or": or_conditions}

    projects_cursor = project_collection.find(query)
    projects = await projects_cursor.to_list(length=100)
    return projects

async def create_new_project(project: ProjectCreate):
    project_dict = project.model_dump() if hasattr(project, "model_dump") else project.dict()
    project_dict["created_at"] = datetime.now(timezone.utc)
    project_dict["updated_at"] = datetime.now(timezone.utc)
    result = await project_collection.insert_one(project_dict)
    
    created_project = await project_collection.find_one({"_id": result.inserted_id})
    return created_project

async def get_single_project(project_id: str):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
        
    project = await project_collection.find_one({"_id": ObjectId(project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    return project

async def update_existing_project(project_id: str, project_update: ProjectUpdate):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")

    update_data = {k: v for k, v in (project_update.model_dump().items() if hasattr(project_update, "model_dump") else project_update.dict().items()) if v is not None}
    
    if len(update_data) >= 1:
        update_data["updated_at"] = datetime.now(timezone.utc)
        update_result = await project_collection.update_one(
            {"_id": ObjectId(project_id)}, {"$set": update_data}
        )
        if update_result.modified_count == 1:
            updated_project = await project_collection.find_one({"_id": ObjectId(project_id)})
            if updated_project:
                return updated_project
                
    # If no modifications were made, return the existing project or 404
    existing_project = await project_collection.find_one({"_id": ObjectId(project_id)})
    if existing_project:
        return existing_project
        
    raise HTTPException(status_code=404, detail="Project not found")

async def delete_existing_project(project_id: str):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
        
    delete_result = await project_collection.delete_one({"_id": ObjectId(project_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")