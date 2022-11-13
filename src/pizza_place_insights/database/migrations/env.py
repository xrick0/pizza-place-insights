# type: ignore
import asyncio
from logging.config import fileConfig
from typing import Tuple, cast

from alembic import context
from alembic.migration import MigrationContext
from alembic.operations.ops import MigrationScript
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine
from sqlalchemy.schema import SchemaItem, Table

from pizza_place_insights import config as app_config
from pizza_place_insights.database.model_base import ModelBase

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Interpret the config file for Python logging.
# This line sets up loggers basically.

database = config.get_main_option("database")

# This section allows to call migrations from code
if database == "default":
    db_uri = db_uri = (
        "postgresql+asyncpg://"
        + f"{app_config.get_settings().db_user}:"
        + f"{app_config.get_settings().db_pass.get_secret_value()}"
        + f"@{app_config.get_settings().db_host}:{app_config.get_settings().db_port}"
        + f"/{app_config.get_settings().db_name}"
    )
    print(db_uri)
    db_schema_name = app_config.get_settings().db_schema_name

    # Interpret the config file for Python logging.
    # This line sets up loggers basically.
    fileConfig(config.config_file_name if config.config_file_name else "")
elif database == "custom":
    db_uri = config.attributes.get("custom_uri")
    db_schema_name = config.attributes.get("custom_schema_name")
else:
    db_uri = db_schema_name = None

if not db_uri or not db_schema_name:
    raise ValueError("Database ou schema não foram definidos.")

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = ModelBase.metadata

config.set_main_option("sqlalchemy.url", str(db_uri).replace("%", "%%"))


def include_object(
    object: SchemaItem, name: str, type_: str, reflected: bool, compare_to: SchemaItem | None
) -> bool:
    if type_ == "table":
        object = cast(Table, object)
        if object.schema == db_schema_name:
            return True
        else:
            return False
    else:
        return True


def process_revision_directives(
    context: MigrationContext, revision: Tuple[str], directives: list[MigrationScript]
) -> None:
    script = directives[0]
    if script.upgrade_ops.is_empty():
        directives[:] = []


def do_run_migrations(connection: AsyncConnection) -> None:
    connection.dialect.default_schema_name = db_schema_name
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        include_object=include_object,
        process_revision_directives=process_revision_directives,
    )
    context.execute(f"SET search_path TO {db_schema_name};")

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    # log.info("Can't run migrations offline")
    ...
else:
    asyncio.run(run_migrations_online())
