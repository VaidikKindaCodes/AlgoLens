from cryptography.fernet import Fernet
from app.core.config import settings


def _get_fernet() -> Fernet:
    key = settings.AI_KEYS_ENCRYPTION_KEY
    if not key:
        raise RuntimeError("AI_KEYS_ENCRYPTION_KEY is not set in environment")
    # settings.AI_KEYS_ENCRYPTION_KEY should be a urlsafe_b64encoded key
    return Fernet(key.encode())


def encrypt(plaintext: str) -> str:
    f = _get_fernet()
    return f.encrypt(plaintext.encode()).decode()


def decrypt(token: str) -> str:
    f = _get_fernet()
    return f.decrypt(token.encode()).decode()
