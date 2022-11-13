from decimal import Decimal

import sqlalchemy as sa
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped

from pizza_place_insights.database.model_base import ModelBase as SABase


class Pizza(SABase):
    __tablename__ = "pizzas"

    id: Mapped[str] = sa.Column(sa.String, primary_key=True)
    pizza_type_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("pizza_types.id"))
    size: Mapped[str] = sa.Column(sa.String)
    price: Mapped[Decimal] = sa.Column(sa.DECIMAL)


class PizzaUpdate(BaseModel):
    id: str = Field(..., alias="pizza_id")
    pizza_type_id: str
    size: str
    price: Decimal
