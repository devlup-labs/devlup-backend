from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Project(BaseModel):
    project_title: str
    project_description: str
    status: str
    type: str
    year: int
    preview_link: Optional[str] = None
    github_repo_link: Optional[str] = None
    docs: Optional[str] = None
    has_issues: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None