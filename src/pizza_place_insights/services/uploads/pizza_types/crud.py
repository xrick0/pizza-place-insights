from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from pizza_place_insights.models.pizza_types import PizzaType, PizzaTypeUpdate


async def upsert(db_sess: AsyncSession, rows: list[PizzaTypeUpdate]) -> None:
    values = [row.dict() for row in rows]

    statement = postgresql.insert(PizzaType).values(values)

    statement = statement.on_conflict_do_update(
        index_elements=["id"],
        set_=dict(
            name=statement.excluded.name,
            category=statement.excluded.category,
            ingredients=statement.excluded.ingredients,
        ),
    )

    await db_sess.execute(statement)
