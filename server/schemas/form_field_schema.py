from pydantic import BaseModel, Field
from typing import Optional

class FormFieldBase(BaseModel):
    name: str
    label: str
    type: str = "text" # e.g., text, email, url
    required: bool = True
    order: int = 0

class FormFieldCreate(FormFieldBase):
    pass

class FormFieldUpdate(BaseModel):
    name: Optional[str] = None
    label: Optional[str] = None
    type: Optional[str] = None
    required: Optional[bool] = None
    order: Optional[int] = None
