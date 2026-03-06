from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectModel(BaseModel):

    project_id: str

    project_title: str
    project_description: str

    status: str
    type: str

    year: int

    preview_link: Optional[str] = None
    github_repo_link: Optional[str] = None

    docs: str

    has_issues: bool

    created_at: datetime
    updated_at: datetime