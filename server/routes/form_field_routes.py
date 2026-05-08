from fastapi import APIRouter, Depends
from typing import List
from server.schemas.form_field_schema import FormFieldCreate, FormFieldUpdate
from server.controllers.form_field_controller import (
    get_form_fields_controller,
    create_form_field_controller,
    get_form_field_controller,
    update_form_field_controller,
    delete_form_field_controller
)
from server.auth import get_admin_user

router = APIRouter(
    prefix="/form-fields",
    tags=["Form Fields"],
)

@router.get("/", response_model=List[dict])
async def get_form_fields():
    return await get_form_fields_controller()

@router.post("/", response_model=dict, dependencies=[Depends(get_admin_user)])
async def create_form_field(field: FormFieldCreate):
    return await create_form_field_controller(field)

@router.get("/{field_id}", response_model=dict, dependencies=[Depends(get_admin_user)])
async def get_form_field(field_id: str):
    return await get_form_field_controller(field_id)

@router.put("/{field_id}", response_model=dict, dependencies=[Depends(get_admin_user)])
async def update_form_field(field_id: str, field: FormFieldUpdate):
    return await update_form_field_controller(field_id, field)

@router.delete("/{field_id}", dependencies=[Depends(get_admin_user)])
async def delete_form_field(field_id: str):
    return await delete_form_field_controller(field_id)
