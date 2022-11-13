import datetime

from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from pizza_place_insights.models.order_details import OrderDetail, OrderDetailInsert
from pizza_place_insights.models.order_imports import OrderImport
from pizza_place_insights.models.orders import Order, OrderInsert

from . import exceptions, iterables


async def bulk_insert(
    db_sess: AsyncSession,
    order_rows: list[OrderInsert],
    order_details_rows: list[OrderDetailInsert],
) -> None:
    order_import = OrderImport(import_datetime=datetime.datetime.now())
    db_sess.add(order_import)
    await db_sess.flush()

    order_import_id = {"order_import_id": order_import.id}

    orders = [dict(**row.dict(), **order_import_id) for row in order_rows]
    order_details = [row.dict() for row in order_details_rows]

    orders_chunk_gen = iterables.chunks(orders, 1000)
    order_details_chunk_gen = iterables.chunks(order_details, 1000)

    try:
        for orders_chunk in orders_chunk_gen:
            statement = postgresql.insert(Order).values(orders_chunk)
            await db_sess.execute(statement)
        for order_details_chunk in order_details_chunk_gen:
            statement = postgresql.insert(OrderDetail).values(order_details_chunk)
            await db_sess.execute(statement)

    except IntegrityError:
        raise exceptions.AlreadyExistsError(
            "Some items of uploaded data already exists on database"
        )
