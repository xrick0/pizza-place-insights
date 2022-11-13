import datetime

import sqlalchemy as sa
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped

from pizza_place_insights.database.model_base import ModelBase as SABase


class Order(SABase):
    __tablename__ = "orders"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    order_import_id = sa.Column(sa.Integer, sa.ForeignKey("order_imports.id", ondelete="CASCADE"))
    date: Mapped[datetime.date] = sa.Column(sa.Date)
    time: Mapped[datetime.time] = sa.Column(sa.Time)


class OrderInsert(BaseModel):
    id: int = Field(..., alias="order_id")
    date: datetime.date
    time: datetime.time
