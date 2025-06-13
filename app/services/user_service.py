"""
User Service.

Encapsulates logic to create a user using hashed passwords.
"""

from app.models.user import User
from app.schemas.user_schema import UserIn
from core.security import hash_password
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(db: AsyncSession, user_data: UserIn) -> User:
    """
    Create a new user with a hashed password.

    Args:
        db (AsyncSession): DB session
        user_data (UserIn): Incoming registration data

    Returns:
        User: Created user instance
    """
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        password=hash_password(user_data.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
