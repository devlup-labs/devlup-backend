from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import List
import jwt
from server.database import project_collection, application_collection, settings_collection
from server.auth import get_admin_user, SECRET_KEY, ALGORITHM

router = APIRouter(tags=["Results & Settings"])

class ShowResultsUpdate(BaseModel):
    value: bool

@router.get("/settings/show_results")
async def get_show_results():
    """
    Public endpoint to check if candidate results are visible.
    """
    setting = await settings_collection.find_one({"key": "show_results"})
    if not setting:
        return {"show_results": False}
    return {"show_results": setting.get("value", False)}

@router.post("/settings/show_results", dependencies=[Depends(get_admin_user)])
async def update_show_results(data: ShowResultsUpdate):
    """
    Admin-only endpoint to toggle candidate results visibility.
    """
    await settings_collection.update_one(
        {"key": "show_results"},
        {"$set": {"value": data.value}},
        upsert=True
    )
    return {"message": "Results visibility updated successfully", "show_results": data.value}

@router.get("/results")
async def get_results(request: Request):
    """
    Public endpoint to fetch the accepted candidates grouped by project.
    Bypasses the visibility check if the request originates from a valid Admin.
    """
    # 1. Fetch show_results setting
    setting = await settings_collection.find_one({"key": "show_results"})
    show_results = setting.get("value", False) if setting else False

    # 2. If results are hidden, verify if user is an admin
    if not show_results:
        is_admin = False
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                if payload.get("role") == "admin":
                    is_admin = True
            except jwt.PyJWTError:
                pass
        
        if not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Results have not been declared yet. Check back soon!"
            )

    # 3. Retrieve all approved ongoing projects
    projects_cursor = project_collection.find({"status": "ongoing", "approval_status": "accepted"})
    projects = await projects_cursor.to_list(length=200)

    # 4. Retrieve all applications where candidate is accepted
    apps_cursor = application_collection.find({
        "$or": [
            {"status_1": "accepted"},
            {"status_2": "accepted"}
        ]
    })
    applications = await apps_cursor.to_list(length=500)

    # 5. Group accepted candidates by project title
    grouped_candidates = {}
    for app in applications:
        name = app.get("mentee_name", "Anonymous Candidate")
        github = app.get("mentee_github_id", "")
        candidate_info = {"name": name, "github": github}

        if app.get("status_1") == "accepted" and app.get("project_name_1"):
            p_name = app["project_name_1"]
            if p_name not in grouped_candidates:
                grouped_candidates[p_name] = []
            grouped_candidates[p_name].append(candidate_info)

        if app.get("status_2") == "accepted" and app.get("project_name_2"):
            p_name = app["project_name_2"]
            if p_name not in grouped_candidates:
                grouped_candidates[p_name] = []
            grouped_candidates[p_name].append(candidate_info)

    # 6. Construct project list payload with candidates joined in
    results = []
    for p in projects:
        title = p.get("project_title")
        if not title:
            continue

        results.append({
            "project_title": title,
            "project_description": p.get("project_description", ""),
            "tech_stack": p.get("tech_stack", []),
            "category": p.get("category", ""),
            "mentors": [
                {
                    "name": m.get("name"),
                    "role": m.get("role", "Project Mentor"),
                    "email": m.get("email"),
                    "linkedin": m.get("linkedin"),
                    "github": m.get("github"),
                    "image_url": m.get("image_url")
                } for m in p.get("mentors", []) if m
            ],
            "accepted_candidates": grouped_candidates.get(title, [])
        })

    return results
