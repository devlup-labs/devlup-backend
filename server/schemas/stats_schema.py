from pydantic import BaseModel, Field
from typing import Optional

class StatBase(BaseModel):
    page: str = Field(...)
    timestamp: str = Field(...)
    sessionId: str = Field(...)
    referrer: Optional[str] = None

class StatCreate(StatBase):
    pass
