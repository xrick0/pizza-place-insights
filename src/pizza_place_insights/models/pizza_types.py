from typing import Any

import sqlalchemy as sa
from pydantic import BaseModel, Field, validator
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped

from pizza_place_insights.database.model_base import ModelBase as SABase


class PizzaType(SABase):
    __tablename__ = "pizza_types"

    id: Mapped[str] = sa.Column(sa.String, primary_key=True)
    name: Mapped[str] = sa.Column(sa.String)
    category: Mapped[str] = sa.Column(sa.String)
    ingredients: Mapped[list[str]] = sa.Column(postgresql.ARRAY(sa.String, dimensions=1))


class PizzaTypeUpdate(BaseModel):
    id: str = Field(..., alias="pizza_type_id")
    name: str
    category: str
    ingredients: list[str]

    @validator("ingredients", pre=True)
    def list_from_comma_separated_string(cls, value: Any) -> Any:
        if isinstance(value, str):
            return [v.strip() for v in value.split(",")]
        return value

    @validator("ingredients")
    def add_cheese_and_sauce_if_missing(cls, value: list[str]) -> Any:
        """Add Tomato Sauce for pizzas with no sauce specified and
        Mozzarella Cheese for those which doesn't specify it.

        Reason for adding sauce:
        "they all include Tomato Sauce, unless another sauce is specified"
        Reason for adding cheese:
        "they all include Mozzarella Cheese, even if not specified"
        Source:
        https://www.kaggle.com/datasets/mysarahmadbhat/pizza-place-sales
        """

        if not any(["Sauce" in ingredient_name for ingredient_name in value]):
            value.append("Tomato Sauce")
        if not any(["Mozzarella Cheese" in ingredient_name for ingredient_name in value]):
            value.append("Mozzarella Cheese")
        return value
