"""
User Repository Layer.

Provides helper functions for querying user data.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Retrieve a user by their email address.

    Args:
        db (AsyncSession): Database session.
        email (str): Email to search for.

    Returns:
        User | None: User object if found, else None.
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def is_email_taken(db: AsyncSession, email: str) -> bool:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first() is not None

