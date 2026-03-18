from pydantic import BaseModel


class PageStatsModel(BaseModel):

    page_id: str

    path: str

    total_views: int
    unique_visitors: int

    period: str