from pydantic import BaseModel
from datetime import datetime

class Stats(BaseModel):
    period: str
    total_views: int
    unique_visitors: int
    period_start: datetime
    period_end: datetime