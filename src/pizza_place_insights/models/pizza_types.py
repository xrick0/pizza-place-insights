import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped

from pizza_place_insights.database.model_base import ModelBase as SABase


class PizzaType(SABase):
    __tablename__ = "pizza_types"

    id: Mapped[str] = sa.Column(sa.String, primary_key=True)
    name: Mapped[str] = sa.Column(sa.String)
    category: Mapped[str] = sa.Column(sa.String)
    ingredients: Mapped[list[str]] = sa.Column(postgresql.ARRAY(sa.String, dimensions=1))
