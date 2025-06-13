from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.auth_service import authenticate_user
from app.schemas.user_schema import UserIn, UserOut
from app.repositories.user_repository import is_email_taken
from app.services.user_service import create_user
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


@router.post("/register", response_model=TokenOut, status_code=201)   # 👈 changed
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
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}



