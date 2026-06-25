from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ApplicationBase(BaseModel):
    model_config = ConfigDict(extra='allow')
    
    mentee_name: Optional[str] = None
    mentee_roll_number: Optional[str] = None
    mentee_github_id: Optional[str] = None
    mentee_email_id: Optional[str] = None
    mentee_proposal_url: Optional[str] = None
    project_name_1: Optional[str] = None
    project_1_proposal: Optional[str] = None
    project_name_2: Optional[str] = None
    project_2_proposal: Optional[str] = None
    status_1: str = "pending"
    status_2: str = "pending"
    created_at: Optional[datetime] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    model_config = ConfigDict(extra='allow')
    mentee_name: Optional[str] = None
    mentee_roll_number: Optional[str] = None
    mentee_github_id: Optional[str] = None
    mentee_email_id: Optional[str] = None
    mentee_proposal_url: Optional[str] = None
    project_name_1: Optional[str] = None
    project_1_proposal: Optional[str] = None
    project_name_2: Optional[str] = None
    project_2_proposal: Optional[str] = None
    status_1: Optional[str] = None
    status_2: Optional[str] = None
    created_at: Optional[datetime] = None