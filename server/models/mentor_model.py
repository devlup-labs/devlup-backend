from pydantic import BaseModel
from datetime import datetime


class MentorModel(BaseModel):

    mentor_id: str

    mentor_name: str
    mentor_email: str

    mentor_github: str
    mentor_linkedin: str

    mentor_description: str
    mentor_image: str

    mentor_role: str

    year: int

    created_at: datetime