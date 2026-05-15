from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserModel(BaseModel):
    model_config = ConfigDict(extra='allow')

    id: str
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    google_id: str
    role: str = "user"
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
