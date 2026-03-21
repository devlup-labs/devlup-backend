from fastapi import APIRouter, status, Depends
from server.schemas.application_schema import ApplicationCreate, ApplicationUpdate
from server.models.application_model import ApplicationModel
from server.auth import get_admin_user
from server.controllers.application_controller import (
    get_applications_controller,
    create_application_controller,
    get_application_controller,
    update_application_controller,
    delete_application_controller
)

router = APIRouter()

# Get all applications
@router.get("/applications", response_model=list[ApplicationModel], dependencies=[Depends(get_admin_user)])
async def get_applications():
    return await get_applications_controller()

# Create a new application
@router.post("/applications", response_model=ApplicationModel, status_code=status.HTTP_201_CREATED)
async def create_application(application: ApplicationCreate):
    return await create_application_controller(application)

# Get an application by ID
@router.get("/applications/{application_id}", response_model=ApplicationModel)
async def get_application(application_id: str):
    return await get_application_controller(application_id)

# Update an application by ID
@router.put("/applications/{application_id}", response_model=ApplicationModel)
async def update_application(application_id: str, application_update: ApplicationUpdate):
    return await update_application_controller(application_id, application_update)

# Delete an application by ID
@router.delete("/applications/{application_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_admin_user)])
async def delete_application(application_id: str):
    return await delete_application_controller(application_id)