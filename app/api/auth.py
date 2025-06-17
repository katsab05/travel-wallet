"""
Auth API

Endpoints for login and register user.
"""


import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories import user_repository
from app.services.auth_service import authenticate_user
from app.schemas.user_schema import UserIn, UserOut
from app.repositories.user_repository import is_email_taken
from app.services.user_service import create_user
from app.utils.email import send_email
from core.security import create_access_token
from app.schemas.token_schema import TokenOut

router = APIRouter()
@router.post("/login", response_model=TokenOut)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    
    """
    Handle user login and return a JWT access token.
    """
    token = await authenticate_user(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=TokenOut, status_code=201)   
async def register_user(
    user_in: UserIn,
    db: AsyncSession = Depends(get_db),
):
    
    """
    Register a new user and return a JWT access token.

    - Checks if the email is already registered.
    - Hashes the password.
    - Creates the user record in the DB.
    - Returns a signed JWT for immediate login.

    Args:
        user_in (UserIn): User registration data
        db (AsyncSession): Async database session

    Returns:
        dict: Access token and token type
    """
    if await is_email_taken(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await create_user(db, user_in)

    # welcome email
    subject = "🎉 Welcome to Travel Wallet"
    body = f"""Hi {user.full_name},

    Thanks for signing up to Travel Wallet! Your travel just got smarter.

    Enjoy your journey!

    – The Travel Wallet Team
    """

    await send_email(user.email, subject, body)
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/password-reset/request")
async def request_password_reset(
    email: EmailStr = Query(...),
    db: AsyncSession = Depends(get_db)
):
    user = await user_repository.get_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = str(uuid.uuid4())  # Normally store this
    reset_link = f"http://localhost:8000/reset-password?token={reset_token}"

    subject = "🔒 Password Reset Request"
    body = f"""Hi {user.full_name},

    We received a request to reset your Travel Wallet password.

    Click the link to reset your password:
    {reset_link}

    If you didn’t request this, you can ignore it.

    – Travel Wallet Security
    """

    await send_email(user.email, subject, body)
    return {"message": "Password reset link sent"}

@router.post("/password-reset/confirm")
async def reset_password(
    token: str = Query(...),
    new_password: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    # Simulate lookup by token
    print(f"[DEBUG] Reset token received: {token}")

    # Simulate updating user
    # In production, you'd verify token and get user_id
    print(f"[DEBUG] Password updated to: {new_password}")

    return {"message": "Password has been reset successfully"}




