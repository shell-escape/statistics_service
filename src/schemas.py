import datetime

from pydantic import BaseModel


class StatOut(BaseModel):
    """Pydantic model for Statistic representation."""

    date: datetime.date
    clicks: int
    views: int
    cost: float
    cpc: float
    cpm: float
