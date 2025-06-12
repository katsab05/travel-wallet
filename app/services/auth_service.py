"""
Authentication Service.

Encapsulates logic for verifying credentials and generating tokens.
"""

from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import get_user_by_email
from core.security import verify_password, create_access_token
from app.models.user import User


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str
) -> str:
    """
    Authenticate a user by email and password.

    Args:
        db (AsyncSession): Active DB session.
        email (str): User's email.
        password (str): Raw password input.

    Raises:
        HTTPException: If credentials are invalid.

    Returns:
        str: JWT token.
    """
    user: User = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email}, timedelta(minutes=30))
    return token
