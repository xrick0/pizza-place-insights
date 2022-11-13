from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from pizza_place_insights.models.pizzas import Pizza, PizzaUpdate


async def upsert(db_sess: AsyncSession, rows: list[PizzaUpdate]) -> None:
    values = [row.dict() for row in rows]

    statement = postgresql.insert(Pizza).values(values)

    statement = statement.on_conflict_do_update(
        index_elements=["id"],
        set_=dict(
            pizza_type_id=statement.excluded.pizza_type_id,
            size=statement.excluded.size,
            price=statement.excluded.price,
        ),
    )

    await db_sess.execute(statement)
