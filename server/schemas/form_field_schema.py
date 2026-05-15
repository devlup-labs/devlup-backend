from pydantic import BaseModel, Field
from typing import Optional, List

class FormFieldBase(BaseModel):
    name: str
    label: str
    type: str = "text" # e.g., text, email, url, number, checkbox, dropdown, project_dropdown
    required: bool = True
    order: int = 0
    options: Optional[List[str]] = None  # For dropdown type: list of option values

class FormFieldCreate(FormFieldBase):
    pass

class FormFieldUpdate(BaseModel):
    name: Optional[str] = None
    label: Optional[str] = None
    type: Optional[str] = None
    required: Optional[bool] = None
    order: Optional[int] = None
    options: Optional[List[str]] = None
