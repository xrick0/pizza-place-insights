from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from pizza_place_insights.models.pizzas import PizzaUpdate
from pizza_place_insights.services.uploads import common
from pizza_place_insights.services.uploads.common.schemas import DefaultResponse

from . import crud


async def update(*, db_sess: AsyncSession, file: UploadFile) -> common.schemas.DefaultResponse:
    rows = await common.csv_parser.parse_and_check(file, PizzaUpdate)

    await crud.upsert(db_sess, rows)

    await db_sess.commit()

    return DefaultResponse(loaded_rows_count=len(rows))
