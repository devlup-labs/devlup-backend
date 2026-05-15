from fastapi import APIRouter, status, Depends, HTTPException
from server.schemas.application_schema import ApplicationCreate, ApplicationUpdate
from server.models.application_model import ApplicationModel
from server.auth import get_admin_user, get_current_user
from server.controllers.application_controller import (
    get_applications_controller,
    create_application_controller,
    get_application_controller,
    update_application_controller,
    delete_application_controller,
    get_application_by_email_controller,
)
from datetime import datetime
import os

router = APIRouter()


def _check_deadline():
    """Raise 403 if the application deadline has passed (IST)."""
    deadline_str = os.getenv("APPLICATION_DEADLINE")
    if deadline_str:
        try:
            from datetime import timezone, timedelta
            IST = timezone(timedelta(hours=5, minutes=30))
            deadline = datetime.fromisoformat(deadline_str).replace(tzinfo=IST)
            now_ist = datetime.now(IST)
            if now_ist > deadline:
                raise HTTPException(
                    status_code=403,
                    detail="The application deadline has passed. Submissions and edits are no longer accepted."
                )
        except ValueError:
            pass  # If the deadline is malformed, don't block


# --- Static routes MUST come before {application_id} ---

# Get application deadline info (public, no auth)
@router.get("/applications/deadline/info")
async def get_deadline_info():
    deadline_str = os.getenv("APPLICATION_DEADLINE", "")
    if not deadline_str:
        return {"deadline": None, "is_open": True}
    try:
        from datetime import timezone, timedelta
        IST = timezone(timedelta(hours=5, minutes=30))
        deadline = datetime.fromisoformat(deadline_str).replace(tzinfo=IST)
        now_ist = datetime.now(IST)
        return {
            "deadline": deadline.isoformat(),
            "is_open": now_ist <= deadline,
        }
    except ValueError:
        return {"deadline": None, "is_open": True}


# Get all applications (admin only)
@router.get("/applications", response_model=list[ApplicationModel], dependencies=[Depends(get_admin_user)])
async def get_applications():
    return await get_applications_controller()


# Get the current user's own application
@router.get("/applications/me", response_model=ApplicationModel)
async def get_my_application(current_user: dict = Depends(get_current_user)):
    email = current_user.get("email", "")
    app = await get_application_by_email_controller(email)
    if not app:
        raise HTTPException(status_code=404, detail="No application found for this user")
    return app


# Create a new application (requires @iitj.ac.in email, one per user, before deadline)
@router.post("/applications", response_model=ApplicationModel, status_code=status.HTTP_201_CREATED)
async def create_application(application: ApplicationCreate, current_user: dict = Depends(get_current_user)):
    email = current_user.get("email", "")
    if not email.endswith("@iitj.ac.in"):
        raise HTTPException(
            status_code=403,
            detail="Only @iitj.ac.in email addresses are allowed to submit applications."
        )

    _check_deadline()

    # Check if this user already has an application
    existing = await get_application_by_email_controller(email)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="You have already submitted an application. You can edit your existing one until the deadline."
        )

    return await create_application_controller(application, email)


# Update the current user's own application (before deadline)
@router.put("/applications/me", response_model=ApplicationModel)
async def update_my_application(application_update: ApplicationUpdate, current_user: dict = Depends(get_current_user)):
    email = current_user.get("email", "")
    if not email.endswith("@iitj.ac.in"):
        raise HTTPException(
            status_code=403,
            detail="Only @iitj.ac.in email addresses are allowed to update applications."
        )

    _check_deadline()

    existing = await get_application_by_email_controller(email)
    if not existing:
        raise HTTPException(status_code=404, detail="No application found for this user")

    return await update_application_controller(existing["id"], application_update)


# --- Dynamic {application_id} routes AFTER all static routes ---

# Get an application by ID
@router.get("/applications/{application_id}", response_model=ApplicationModel)
async def get_application(application_id: str):
    return await get_application_controller(application_id)


# Update an application by ID (admin only)
@router.put("/applications/{application_id}", response_model=ApplicationModel, dependencies=[Depends(get_admin_user)])
async def update_application(application_id: str, application_update: ApplicationUpdate):
    return await update_application_controller(application_id, application_update)


# Delete an application by ID (admin only)
@router.delete("/applications/{application_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_admin_user)])
async def delete_application(application_id: str):
    return await delete_application_controller(application_id)