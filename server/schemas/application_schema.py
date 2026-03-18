from pydantic import BaseModel
from datetime import datetime

class Application(BaseModel):
    mentee_name: str
    mentee_roll_number: str
    mentee_github_id: str
    mentee_email_id: str
    created_at: datetime