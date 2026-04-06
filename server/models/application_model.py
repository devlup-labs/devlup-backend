from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ApplicationModel(BaseModel):
    id: str
    mentee_name: str
    mentee_roll_number: str
    mentee_github_id: str
    mentee_email_id: str
    mentee_proposal_url: Optional[str] = None
    project_name_1: Optional[str] = None
    project_name_2: Optional[str] = None
    status_1: Optional[str] = "pending"
    status_2: Optional[str] = "pending"
    created_at: Optional[datetime] = None