from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StatsSchema(BaseModel):
    period: str
    total_views: int
    unique_visitors: int
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None