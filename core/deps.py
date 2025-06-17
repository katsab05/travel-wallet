"""
Dependency Injection for the authenticated user.
"""

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import get_settings
from app.db.session import get_db
from app.repositories.user_repository import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    """
    Decode JWT, fetch the user from the database,
    or raise 401 if anything is invalid.
    """
    settings = get_settings()                         
    credentials_exc = HTTPException(
        status_code=401, detail="Invalid credentials"
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc

    user = await get_user_by_email(db, email)
    if user is None:
        raise credentials_exc

    return user
