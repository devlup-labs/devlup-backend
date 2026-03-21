from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicationBase(BaseModel):
    mentee_name: str
    mentee_roll_number: str
    mentee_github_id: str
    mentee_email_id: str
    mentee_proposal_url: str
    created_at: Optional[datetime] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    mentee_name: Optional[str] = None
    mentee_roll_number: Optional[str] = None
    mentee_github_id: Optional[str] = None
    mentee_email_id: Optional[str] = None
    mentee_proposal_url: Optional[str] = None
    created_at: Optional[datetime] = None