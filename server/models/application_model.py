from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ApplicationModel(BaseModel):
    model_config = ConfigDict(extra='allow')
    
    id: str
    mentee_name: Optional[str] = None
    mentee_roll_number: Optional[str] = None
    mentee_github_id: Optional[str] = None
    mentee_email_id: Optional[str] = None
    mentee_proposal_url: Optional[str] = None
    project_name_1: Optional[str] = None
    project_name_2: Optional[str] = None
    status_1: Optional[str] = "pending"
    status_2: Optional[str] = "pending"
    created_at: Optional[datetime] = None