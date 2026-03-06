from pydantic import BaseModel
from datetime import date


class TimelineModel(BaseModel):

    time_id: str

    timeline_topic: str

    start_date: date
    end_date: date

    timeline_description: str