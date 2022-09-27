import datetime
from typing import Any, Generator, Optional

import src.db.models as dbm
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src import config

engine = create_engine(
    config.DB_URI,
    pool_use_lifo=True,
    pool_pre_ping=True,
)

LocalSession = sessionmaker(bind=engine, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    """Get session to work with the db."""
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()


def get_stat_by_date(session: Session, date: datetime.date) -> dbm.Stat:
    """Gets day statistic for specific date."""
    return session.get(dbm.Stat, date)


def get_stat(
    session: Session,
    from_: Optional[datetime.date] = None,
    to_: Optional[datetime.date] = None,
) -> list[dbm.Stat]:
    """Gets list of day stats in [from_, to_] date range."""
    query = session.query(dbm.Stat)
    if from_ is not None:
        query = query.filter(from_ <= dbm.Stat.date)
    if to_ is not None:
        query = query.filter(dbm.Stat.date <= to_)
    return query.all()


def add_day_stat(session: Session, day_stat: dbm.Stat) -> None:
    """Add Stat instance to the db."""
    session.add(day_stat)
    session.commit()


def update_stat(
    session: Session,
    date: datetime.date,
    args: dict[str, Any],
) -> None:
    """Updates 'args' fields of Stat table instance with date = 'date'."""
    session.query(dbm.Stat).filter(dbm.Stat.date == date).update(
        args, synchronize_session=False
    )
    session.commit()


def delete_stat(
    session: Session,
    from_: Optional[datetime.date] = None,
    to_: Optional[datetime.date] = None,
) -> None:
    """Deletes stat from the db."""
    stat = get_stat(session, from_, to_)
    for day_stat in stat:
        session.delete(day_stat)
    session.commit()
