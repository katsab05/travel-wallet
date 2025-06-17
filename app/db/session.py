
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from core.config import get_settings

DATABASE_URL: str = get_settings().DATABASE_URL     


engine = create_async_engine(DATABASE_URL, echo=True)


async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a database session per request and ensures it’s closed.
    """
    async with async_session_maker() as session:
        yield session
