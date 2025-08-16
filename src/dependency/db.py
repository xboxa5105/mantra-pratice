from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from dependency.setting import get_settings

settings = get_settings()

DATABASE_URL = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"

kwargs = {
    "echo": False,
    "pool_pre_ping": True,
    "pool_recycle": 1500,
    "pool_size": 1,
    "max_overflow": 1,
}


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    engine = create_async_engine(DATABASE_URL, **kwargs)

    async_session = async_sessionmaker(
        bind=engine,
    )
    async with async_session() as session:
        yield session
