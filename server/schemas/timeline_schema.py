from pydantic import BaseModel
from typing import Optional

class TimelineCreate(BaseModel):
    timeline_topic: str
    program_name: str
    start_date: str
    end_date: Optional[str] = None
    timeline_description: str

class TimelineUpdate(BaseModel):
    timeline_topic: Optional[str] = None
    program_name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    timeline_description: Optional[str] = None
