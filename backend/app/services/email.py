import hmac
import hashlib
from datetime import datetime, timezone
from typing import Any

import requests

from app.core.config import settings

RESEND_API_URL = "https://api.resend.com/emails"


def send_otp_email(email: str, otp: str) -> None:
    payload = {
        "from": settings.EMAIL_FROM,
        "to": [email],
        "subject": "Your AlgoLens verification code",
        "html": f"<p>Your verification code is <strong>{otp}</strong>. It expires in {settings.OTP_EXPIRE_MINUTES} minutes.</p>",
    }
    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(RESEND_API_URL, json=payload, headers=headers, timeout=15)
    response.raise_for_status()


def hash_otp(otp: str) -> str:
    return hmac.new(settings.SECRET_KEY.encode(), otp.encode(), hashlib.sha256).hexdigest()


def verify_otp_hash(otp: str, otp_hash: str) -> bool:
    return hmac.compare_digest(hash_otp(otp), otp_hash)
