import sqlalchemy as sa
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class Stat(Base):
    __tablename__ = "statistic"

    date = sa.Column(sa.Date, nullable=False, primary_key=True)
    views = sa.Column(sa.Integer, nullable=False, default=0)
    clicks = sa.Column(sa.Integer, nullable=False, default=0)
    cost = sa.Column(sa.Float, nullable=False, default=0)
