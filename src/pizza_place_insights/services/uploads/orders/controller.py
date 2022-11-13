from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from pizza_place_insights.models.order_details import OrderDetailInsert
from pizza_place_insights.models.orders import OrderInsert
from pizza_place_insights.services.uploads import common
from pizza_place_insights.services.uploads.common.schemas import DefaultResponse
from pizza_place_insights.services.uploads.orders.exceptions import InvalidFileCombinationError

from . import crud


async def create(
    *, db_sess: AsyncSession, files: list[UploadFile]
) -> common.schemas.DefaultResponse:
    if len(files) != 2:
        raise InvalidFileCombinationError("This upload must contain 2 files")

    mapped_files = {file.filename: file for file in files}

    if "orders.csv" not in mapped_files or "order_details.csv" not in mapped_files:
        raise InvalidFileCombinationError(
            "Files must be named 'orders.csv' and 'order_details.csv'"
        )

    orders_rows = await common.csv_parser.parse_and_check(mapped_files["orders.csv"], OrderInsert)
    order_details_rows = await common.csv_parser.parse_and_check(
        mapped_files["order_details.csv"], OrderDetailInsert
    )

    await crud.bulk_insert(db_sess, order_rows=orders_rows, order_details_rows=order_details_rows)

    await db_sess.commit()

    return DefaultResponse(loaded_rows_count=len(orders_rows))
