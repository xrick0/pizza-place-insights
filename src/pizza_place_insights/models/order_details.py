import sqlalchemy as sa
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped

from pizza_place_insights.database.model_base import ModelBase as SABase


class OrderDetail(SABase):
    __tablename__ = "order_details"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    pizza_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("pizzas.id"))
    order_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("orders.id"))
    quantity: Mapped[int] = sa.Column(sa.Integer)


class OrderDetailInsert(BaseModel):
    id: int = Field(..., alias="order_details_id")
    pizza_id: str
    order_id: int
    quantity: int
