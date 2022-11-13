import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped

from pizza_place_insights.database.model_base import ModelBase as SABase


class OrderImport(SABase):
    __tablename__ = "order_imports"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    import_datetime: Mapped[datetime.datetime] = sa.Column(sa.DateTime)
