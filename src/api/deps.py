from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.exceptions import CredentialsException
from src.core.security import decode_token
from src.db.session import get_db
from src.models import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Get the current authenticated user."""
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise CredentialsException("Invalid token")

    if payload.get("type") != "access":
        raise CredentialsException("Invalid token type")

    user_id = payload.get("sub")
    if user_id is None:
        raise CredentialsException("Invalid token payload")

    user = db.execute(select(User).where(User.id == int(user_id))).scalar_one_or_none()

    if user is None:
        raise CredentialsException("User not found")

    if not user.is_active:
        raise CredentialsException("User is inactive")

    return user
