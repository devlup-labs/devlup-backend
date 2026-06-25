from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from typing import List, Optional
from server.projects_website.auth import get_current_user
from server.core.database import project_collection, application_collection
from server.projects_website.models.application_model import ApplicationModel
from server.projects_website.models.project_model import ProjectModel
from server.projects_website.schemas.application_schema import ApplicationUpdate

router = APIRouter(prefix="/mentor", tags=["Mentor Panel"])

async def get_current_mentor(current_user: dict = Depends(get_current_user)):
    """
    Dependency to verify if the authenticated Google user is a mentor of a live project.
    Allows admins to access these endpoints for testing purposes.
    """
    email = current_user.get("email")
    role = current_user.get("role")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication email is missing"
        )

    # Check if the user is a mentor of a live project (ongoing and accepted)
    live_project = await project_collection.find_one({
        "status": "ongoing",
        "approval_status": "accepted",
        "mentors.email": email
    })

    if not live_project and role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You are not registered as an active mentor for any live projects."
        )

    return current_user


@router.get("/projects", response_model=List[ProjectModel])
async def get_mentor_projects(current_user: dict = Depends(get_current_mentor)):
    """
    Get all live, accepted projects mentored by the currently authenticated user.
    """
    email = current_user.get("email")
    role = current_user.get("role")

    query = {"status": "ongoing", "approval_status": "accepted"}
    if role != "admin":
        query["mentors.email"] = email

    projects_cursor = project_collection.find(query)
    projects = await projects_cursor.to_list(length=100)
    return projects


@router.get("/applications")
async def get_mentor_applications(current_user: dict = Depends(get_current_mentor)):
    """
    Get applications for the projects mentored by this user.
    Strictly filters out non-relevant project choices and details from the payload.
    """
    email = current_user.get("email")
    role = current_user.get("role")

    # 1. Fetch mentor's projects to get their titles
    proj_query = {"status": "ongoing", "approval_status": "accepted"}
    if role != "admin":
        proj_query["mentors.email"] = email

    mentor_projects = await project_collection.find(proj_query).to_list(length=100)
    mentor_project_titles = [p["project_title"] for p in mentor_projects if "project_title" in p]

    if not mentor_project_titles and role != "admin":
        return []

    # 2. Query applications matching any of those projects
    if role == "admin":
        app_query = {}
    else:
        app_query = {
            "$or": [
                {"project_name_1": {"$in": mentor_project_titles}},
                {"project_name_2": {"$in": mentor_project_titles}}
            ]
        }

    applications = []
    cursor = application_collection.find(app_query)

    async for app in cursor:
        app["id"] = str(app["_id"])
        del app["_id"]

        # If user is admin, they see everything; otherwise, mask non-relevant project data on-the-fly
        if role != "admin":
            # Mask Choice 1 if not mentored by this user
            if app.get("project_name_1") not in mentor_project_titles:
                app["project_name_1"] = None
                app["project_1_proposal"] = None
                app["mentee_proposal_url"] = None
                app["mentee_prposoal_url"] = None
                app["status_1"] = None
            
            # Mask Choice 2 if not mentored by this user
            if app.get("project_name_2") not in mentor_project_titles:
                app["project_name_2"] = None
                app["project_2_proposal"] = None
                app["mentee_proposal_url2"] = None
                app["status_2"] = None

        applications.append(app)

    return applications


@router.put("/applications/{application_id}")
async def update_mentor_application(
    application_id: str,
    application_update: ApplicationUpdate,
    current_user: dict = Depends(get_current_mentor)
):
    """
    Update application status (Accept/Reject) for the mentor's specific project only.
    Strictly rejects status updates for projects not mentored by this user.
    """
    if not ObjectId.is_valid(application_id):
        raise HTTPException(status_code=400, detail="Invalid application ID")

    email = current_user.get("email")
    role = current_user.get("role")

    # 1. Fetch the application
    app = await application_collection.find_one({"_id": ObjectId(application_id)})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    # 2. Fetch mentor's live projects
    proj_query = {"status": "ongoing", "approval_status": "accepted"}
    if role != "admin":
        proj_query["mentors.email"] = email

    mentor_projects = await project_collection.find(proj_query).to_list(length=100)
    mentor_project_titles = [p["project_title"] for p in mentor_projects if "project_title" in p]

    update_payload = application_update.model_dump(exclude_unset=True)
    clean_update = {}

    # 3. Strictly validate each status change
    if "status_1" in update_payload:
        if role == "admin" or app.get("project_name_1") in mentor_project_titles:
            clean_update["status_1"] = update_payload["status_1"]
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You are not registered as a mentor for the first project choice."
            )

    if "status_2" in update_payload:
        if role == "admin" or app.get("project_name_2") in mentor_project_titles:
            clean_update["status_2"] = update_payload["status_2"]
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You are not registered as a mentor for the second project choice."
            )

    # 4. Apply status update if validated
    if clean_update:
        from datetime import datetime
        clean_update["updated_at"] = datetime.utcnow()
        await application_collection.update_one(
            {"_id": ObjectId(application_id)},
            {"$set": clean_update}
        )

    # 5. Fetch and return masked updated application
    updated_app = await application_collection.find_one({"_id": ObjectId(application_id)})
    updated_app["id"] = str(updated_app["_id"])
    del updated_app["_id"]

    if role != "admin":
        if updated_app.get("project_name_1") not in mentor_project_titles:
            updated_app["project_name_1"] = None
            updated_app["project_1_proposal"] = None
            updated_app["mentee_proposal_url"] = None
            updated_app["mentee_prposoal_url"] = None
            updated_app["status_1"] = None
        if updated_app.get("project_name_2") not in mentor_project_titles:
            updated_app["project_name_2"] = None
            updated_app["project_2_proposal"] = None
            updated_app["mentee_proposal_url2"] = None
            updated_app["status_2"] = None

    return updated_app
