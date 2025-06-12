from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.auth_service import authenticate_user
from app.schemas.user_schema import UserIn, UserOut
from app.repositories.user_repository import is_email_taken
from app.services.user_service import create_user

router = APIRouter()

@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle user login and return a JWT access token.
    """
    token = await authenticate_user(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserOut)
async def register_user(
    user_in: UserIn,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.

    Returns:
        UserOut: Public user info
    """
    if await is_email_taken(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await create_user(db, user_in)
    return user