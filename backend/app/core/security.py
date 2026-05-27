import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from uuid import uuid4

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

TokenType = Literal["access", "refresh"]
password_hash = PasswordHash.recommended()
DUMMY_PASSWORD_HASH = password_hash.hash("not-the-user-password")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_token(
    subject: int,
    token_type: TokenType,
    expires_delta: timedelta,
) -> tuple[str, str, datetime]:
    now = datetime.now(timezone.utc)
    expires_at = now + expires_delta
    jti = str(uuid4())
    payload = {
        "sub": str(subject),
        "type": token_type,
        "jti": jti,
        "iat": now,
        "exp": expires_at,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token, jti, expires_at


def create_access_token(user_id: int) -> str:
    token, _, _ = create_token(
        user_id,
        "access",
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return token


def create_refresh_token(user_id: int) -> tuple[str, str, datetime]:
    return create_token(
        user_id,
        "refresh",
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])


def hash_jti(jti: str) -> str:
    return hashlib.sha256(jti.encode("utf-8")).hexdigest()
