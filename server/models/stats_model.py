from pydantic import BaseModel
from datetime import date


class StatsModel(BaseModel):

    stat_id: str

    period: str

    total_views: int
    unique_visitors: int

    period_start: date
    period_end: date