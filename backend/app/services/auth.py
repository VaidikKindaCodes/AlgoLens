from datetime import datetime, timezone

from fastapi import HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy import or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    DUMMY_PASSWORD_HASH,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_jti,
    hash_password,
    verify_password,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.ai_credentials import AICredentialService

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password",
    headers={"WWW-Authenticate": "Bearer"},
)
INVALID_REFRESH_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired refresh token",
    headers={"WWW-Authenticate": "Bearer"},
)


def register_user(db: Session, data: RegisterRequest) -> User:
    duplicate = db.scalar(
        select(User).where(
            or_(User.email == str(data.email), User.username == data.username)
        )
    )
    if duplicate:
        field = "email" if duplicate.email == str(data.email) else "username"
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An account with that {field} already exists",
        )

    user = User(
        email=str(data.email),
        username=data.username,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with that email or username already exists",
        ) from None
    db.refresh(user)

    return user


def authenticate_user(db: Session, data: LoginRequest) -> User:
    user = db.scalar(select(User).where(User.email == str(data.email)))
    if not user:
        verify_password(data.password, DUMMY_PASSWORD_HASH)
        raise INVALID_CREDENTIALS
    if not verify_password(data.password, user.password_hash):
        raise INVALID_CREDENTIALS
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )
    return user


def issue_token_pair(db: Session, user: User) -> TokenResponse:
    access_token = create_access_token(user.id)
    refresh_token, jti, expires_at = create_refresh_token(user.id)
    db.add(
        RefreshToken(
            jti_hash=hash_jti(jti),
            user_id=user.id,
            expires_at=expires_at,
        )
    )
    db.commit()
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user,
    )


def rotate_refresh_token(db: Session, raw_token: str) -> TokenResponse:
    try:
        payload = decode_token(raw_token)
        if payload.get("type") != "refresh":
            raise INVALID_REFRESH_TOKEN
        user_id = int(payload["sub"])
        token_hash = hash_jti(payload["jti"])
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        raise INVALID_REFRESH_TOKEN from None

    stored_token = db.scalar(
        select(RefreshToken).where(RefreshToken.jti_hash == token_hash)
    )
    now = datetime.now(timezone.utc)
    if (
        not stored_token
        or stored_token.revoked_at is not None
        or _as_utc(stored_token.expires_at) <= now
        or stored_token.user_id != user_id
    ):
        raise INVALID_REFRESH_TOKEN

    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise INVALID_REFRESH_TOKEN

    stored_token.revoked_at = now
    return issue_token_pair(db, user)


def revoke_refresh_token(db: Session, raw_token: str) -> None:
    try:
        payload = decode_token(raw_token)
        if payload.get("type") != "refresh":
            return
        token_hash = hash_jti(payload["jti"])
    except (InvalidTokenError, KeyError, TypeError):
        return

    stored_token = db.scalar(
        select(RefreshToken).where(RefreshToken.jti_hash == token_hash)
    )
    if stored_token and stored_token.revoked_at is None:
        stored_token.revoked_at = datetime.now(timezone.utc)
        db.commit()


def revoke_all_user_tokens(db: Session, user_id: int) -> None:
    db.execute(
        update(RefreshToken)
        .where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked_at.is_(None),
        )
        .values(revoked_at=datetime.now(timezone.utc))
    )
    db.commit()


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
