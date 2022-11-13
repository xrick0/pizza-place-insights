import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped

from pizza_place_insights.database.model_base import ModelBase as SABase


class Order(SABase):
    __tablename__ = "orders"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    date: Mapped[datetime.date] = sa.Column(sa.Date)
    time: Mapped[datetime.time] = sa.Column(sa.Time)
