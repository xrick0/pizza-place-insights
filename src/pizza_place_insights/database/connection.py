import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from pizza_place_insights.config import get_settings

log = logging.getLogger(__name__)

log.debug("Configuring SQLAlchemy connection")
schema_translate_map = {
    None: get_settings().db_schema_name,
}

db_uri = (
    "postgresql+asyncpg://"
    + f"{get_settings().db_user}:{get_settings().db_pass.get_secret_value()}"
    + f"@{get_settings().db_host}:{get_settings().db_port}/{get_settings().db_name}"
)

engine = (
    create_async_engine(
        db_uri,
        pool_pre_ping=True,
        echo=get_settings().dev_sqlalchemy_echo,
    ).execution_options(schema_translate_map=schema_translate_map),
)


log.debug("Definindo sessionmakers")
session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db_sess() -> AsyncGenerator[AsyncSession, None]:
    db_sess: AsyncSession = session()
    try:
        yield db_sess
    finally:
        await db_sess.close()
