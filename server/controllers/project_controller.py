from fastapi import HTTPException, status
from typing import List, Optional
from bson import ObjectId
from datetime import datetime, timezone

from server.database import project_collection, mentor_collection
from server.schemas.project_schema import ProjectCreate, ProjectUpdate
import urllib.parse

async def sync_project_mentors(project: dict):
    mentors = project.get("mentors", [])
    year = project.get("year", datetime.now().year)
    for m in mentors:
        # Check if m is a dict or a MentorBase object
        m_name = m.get("name") if isinstance(m, dict) else getattr(m, "name", None)
        if not m_name:
            continue
            
        # Avoid duplication by name and year
        existing = await mentor_collection.find_one({"name": m_name, "year": year})
        if not existing:
            m_github = m.get("github") if isinstance(m, dict) else getattr(m, "github", "")
            m_email = m.get("email") if isinstance(m, dict) else getattr(m, "email", "")
            m_linkedin = m.get("linkedin") if isinstance(m, dict) else getattr(m, "linkedin", "")
            m_role = m.get("role") if isinstance(m, dict) else getattr(m, "role", "Project Mentor")
            
            # Generate avatar URL using initials (matching existing mentors)
            safe_name = urllib.parse.quote_plus(m_name)
            avatar_url = f"https://api.dicebear.com/7.x/initials/svg?seed={safe_name}"
            
            new_mentor = {
                "name": m_name,
                "github": m_github or "",
                "email": m_email or "",
                "description": "DevlUp Project Mentor",
                "linkedin": m_linkedin or "",
                "image": avatar_url,
                "role": m_role or "Project Mentor",
                "year": year
            }
            await mentor_collection.insert_one(new_mentor)

async def get_all_projects(status: Optional[str] = None, has_issues: Optional[bool] = None, type: Optional[str] = None, year: Optional[int] = None, approval_status: Optional[str] = None):
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
        
    if approval_status is not None:
        if approval_status == "accepted":
            status_query = {"$or": [{"approval_status": "accepted"}, {"approval_status": {"$exists": False}}]}
        else:
            status_query = {"approval_status": approval_status}
            
        if or_conditions:
            query["$and"] = [{"$or": or_conditions}, status_query]
        else:
            query.update(status_query)
    elif or_conditions:
        query["$or"] = or_conditions

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

async def submit_public_project(project: ProjectCreate):
    project_dict = project.model_dump() if hasattr(project, "model_dump") else project.dict()
    project_dict["created_at"] = datetime.now(timezone.utc)
    project_dict["updated_at"] = datetime.now(timezone.utc)
    project_dict["approval_status"] = "pending"
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
                # Sync mentors if project is accepted
                if updated_project.get("approval_status") == "accepted":
                    await sync_project_mentors(updated_project)
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