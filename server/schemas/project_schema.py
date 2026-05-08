from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class MentorBase(BaseModel):
    name: str
    role: Optional[str] = "Project Mentor"
    email: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class ProjectBase(BaseModel):
    project_title: str = Field(...)
    project_description: str = Field(...)
    status: str = Field(..., description="ongoing/completed/archived")
    type: str = Field(..., description="woc/soc")
    year: int = Field(...)
    preview_link: Optional[str] = None
    github_repo_link: Optional[str] = None
    docs: str = Field(default="")
    is_docs_accessible: bool = Field(default=False)
    has_issues: bool = Field(default=False)
    approval_status: str = Field(default="accepted", description="pending/accepted/rejected")
    
    # Extended fields for Google Sheets compatibility
    tech_stack: Optional[list[str]] = Field(default=[])
    mentors: Optional[list[MentorBase]] = Field(default=[])
    industry_mentor: Optional[MentorBase] = None
    category: Optional[str] = None
    current_desc: Optional[str] = None
    live_links: Optional[list[str]] = Field(default=[])
    recommended: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    project_title: Optional[str] = None
    project_description: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    year: Optional[int] = None
    preview_link: Optional[str] = None
    github_repo_link: Optional[str] = None
    docs: Optional[str] = None
    is_docs_accessible: Optional[bool] = None
    has_issues: Optional[bool] = None
    approval_status: Optional[str] = None
    
    tech_stack: Optional[list[str]] = None
    mentors: Optional[list[MentorBase]] = None
    industry_mentor: Optional[MentorBase] = None
    category: Optional[str] = None
    current_desc: Optional[str] = None
    live_links: Optional[list[str]] = None
    recommended: Optional[str] = None