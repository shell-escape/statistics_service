import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator

import src.db.models as dbm
from src import schemas
from src.db import service


class DayStat(BaseModel):
    date: datetime.date
    views = 0
    clicks = 0
    cost = 0.0

    def _to_orm(self) -> dbm.Stat:
        """Creates Stat ORM instance from DayStat object."""
        return dbm.Stat(
            date=self.date, views=self.views, clicks=self.clicks, cost=self.cost
        )

    def _form_update_dict(self, current_db_day_stat: dbm.Stat):
        return {
            dbm.Stat.clicks: current_db_day_stat.clicks + self.clicks,
            dbm.Stat.views: current_db_day_stat.views + self.views,
            dbm.Stat.cost: current_db_day_stat.cost + self.cost,
        }

    def add_to_db(self, session):
        """Adds instance to the db."""
        stat_orm = self._to_orm()
        service.add_day_stat(session, stat_orm)

    def update(self, session, current_db_day_stat):
        """Updates db instance with such date as 'self.date'."""
        update_args = self._form_update_dict(current_db_day_stat)
        service.update_stat(session, self.date, update_args)

    @validator("clicks", "views", "cost")
    def nonnegative(  # pylint: disable=E0213
        cls, v: Optional[Union[int, float]]
    ) -> Optional[str]:
        """Non-negative validator"""
        if v < 0:
            raise ValueError("Should be positive")
        return v


def get_stat_view(stats: list[dbm.Stat]) -> list[schemas.StatOut]:
    """Creates representation of day statistic, i.e. adds cpc and cpm."""
    stats_view = []
    for stat in stats:
        stat_view = {}
        stat_view["date"] = stat.date
        stat_view["clicks"] = stat.clicks
        stat_view["views"] = stat.views
        stat_view["cost"] = stat.cost
        stat_view["cpc"] = 0 if stat.clicks == 0 else round(stat.cost / stat.clicks, 2)
        stat_view["cpm"] = (
            0 if stat.views == 0 else round(stat.cost / stat.views * 1000, 2)
        )
        stats_view.append(schemas.StatOut(**stat_view))
    return stats_view
