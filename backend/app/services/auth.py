import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import requests
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
from app.schemas.auth import (
    GoogleAuthRequest,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    ResendOtpRequest,
    TokenResponse,
    UserResponse,
    VerifyOtpRequest,
)
from app.services.email import send_otp_email

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


def _generate_otp(length: int) -> str:
    return "".join(str(secrets.randbelow(10)) for _ in range(length))


def _hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode("utf-8") + settings.SECRET_KEY.encode("utf-8")).hexdigest()


def _sanitize_username(value: str) -> str:
    sanitized = "".join(ch.lower() if ch.isalnum() else "_" for ch in value)
    sanitized = sanitized.strip("_")
    if len(sanitized) < 3:
        sanitized = f"user_{secrets.token_hex(3)}"
    return sanitized[:32]


def _find_unique_username(db: Session, base: str) -> str:
    username = _sanitize_username(base)
    existing = db.scalar(select(User).where(User.username == username))
    suffix = 1
    while existing:
        candidate = f"{username[:28]}_{suffix}"
        existing = db.scalar(select(User).where(User.username == candidate))
        if not existing:
            return candidate
        suffix += 1
    return username


def _send_verification_code(user: User, db: Session) -> None:
    otp = _generate_otp(settings.OTP_LENGTH)
    user.otp_code_hash = _hash_otp(otp)
    user.otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    db.commit()
    send_otp_email(user.email, otp)


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
        email_verified=False,
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
    _send_verification_code(user, db)
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
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required",
        )
    return user


def verify_otp(db: Session, data: VerifyOtpRequest) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == str(data.email)))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified",
        )
    if not user.otp_code_hash or not user.otp_expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No verification code found. Please request a new code.",
        )
    if user.otp_expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code has expired",
        )
    if _hash_otp(data.code) != user.otp_code_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code",
        )
    user.email_verified = True
    user.otp_code_hash = None
    user.otp_expires_at = None
    db.commit()
    return issue_token_pair(db, user)


def resend_otp(db: Session, data: ResendOtpRequest) -> None:
    user = db.scalar(select(User).where(User.email == str(data.email)))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified",
        )
    _send_verification_code(user, db)


def _get_google_user_info(code: str) -> dict[str, Any]:
    token_response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        timeout=15,
    )
    token_response.raise_for_status()
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to obtain Google access token",
        )
    user_info_response = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    user_info_response.raise_for_status()
    return user_info_response.json()


def get_google_login_url() -> str:
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }
    query = "&".join(f"{key}={requests.utils.quote(str(value))}" for key, value in params.items())
    return f"https://accounts.google.com/o/oauth2/v2/auth?{query}"


def resolve_google_user(db: Session, user_info: dict[str, Any]) -> User:
    email = user_info.get("email")
    google_id = user_info.get("sub")
    verified = user_info.get("email_verified")
    if not email or not google_id or verified is not True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google email verification failed",
        )
    email = str(email).lower()
    user = db.scalar(
        select(User).where(
            or_(User.google_id == google_id, User.email == email)
        )
    )
    if user:
        if user.google_id and user.google_id != google_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A different Google account is already linked to this user",
            )
        user.google_id = google_id
        user.email_verified = True
        db.commit()
        return user

    username = _find_unique_username(email.split("@", 1)[0])
    password_hash = hash_password(secrets.token_hex(32))
    user = User(
        email=email,
        username=username,
        password_hash=password_hash,
        email_verified=True,
        google_id=google_id,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        user = db.scalar(select(User).where(User.email == email))
        if user:
            return user
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unable to create Google account",
        )
    db.refresh(user)
    return user


def authenticate_google_user(db: Session, code: str) -> TokenResponse:
    user_info = _get_google_user_info(code)
    user = resolve_google_user(db, user_info)
    return issue_token_pair(db, user)


def issue_token_pair(db: Session, user: User) -> TokenResponse:
    access_token = create_access_token(user.id)
    refresh_token, jti, expires_at = create_refresh_token(user.id)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )
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
