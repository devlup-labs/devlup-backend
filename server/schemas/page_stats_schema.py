from pydantic import BaseModel

class PageStatsSchema(BaseModel):
    path: str
    total_views: int
    unique_visitors: int
    period: str