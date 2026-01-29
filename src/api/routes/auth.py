from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.exceptions import BadRequestException, ConflictException, CredentialsException
from src.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from src.db.session import get_db
from src.models import User
from src.schemas.user import RefreshTokenRequest, TokenResponse, UserCreate, UserLogin, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> User:
    """Register a new user."""
    existing_email = db.execute(
        select(User).where(User.email == user_in.email)
    ).scalar_one_or_none()
    if existing_email:
        raise ConflictException("Email already registered")

    existing_username = db.execute(
        select(User).where(User.username == user_in.username)
    ).scalar_one_or_none()
    if existing_username:
        raise ConflictException("Username already taken")

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        username=user_in.username,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(user_in: UserLogin, db: Session = Depends(get_db)) -> dict:
    """Login and get tokens."""
    user = db.execute(select(User).where(User.email == user_in.email)).scalar_one_or_none()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise BadRequestException("Invalid email or password")

    if not user.is_active:
        raise BadRequestException("User account is disabled")

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: RefreshTokenRequest, db: Session = Depends(get_db)) -> dict:
    """Refresh access token."""
    payload = decode_token(request.refresh_token)

    if payload is None:
        raise CredentialsException("Invalid refresh token")

    if payload.get("type") != "refresh":
        raise CredentialsException("Invalid token type")

    user_id = payload.get("sub")
    if user_id is None:
        raise CredentialsException("Invalid token payload")

    user = db.execute(select(User).where(User.id == int(user_id))).scalar_one_or_none()

    if user is None or not user.is_active:
        raise CredentialsException("User not found or inactive")

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }
