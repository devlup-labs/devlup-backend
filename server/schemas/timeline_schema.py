from pydantic import BaseModel
from datetime import date

class Timeline(BaseModel):
    timeline_topic: str
    start_date: date
    end_date: date
    timeline_description: str