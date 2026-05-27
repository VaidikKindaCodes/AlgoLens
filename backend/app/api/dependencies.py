from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.database import get_db
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)
DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(bearer_scheme)
    ],
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not credentials or credentials.scheme.lower() != "bearer":
        raise unauthorized
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise unauthorized
        user_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        raise unauthorized from None

    user = db.get(User, user_id)
    if not user:
        raise unauthorized
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
