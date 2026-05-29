from sqlalchemy.orm import Session
from app.models.ai_credential import AICredential
from app.utils.crypto import encrypt, decrypt
from datetime import datetime

DEFAULT_MODELS = {
    "gemini": "models/gemini-2.0-flash",
    "openai": "gpt-4o-mini",
    "huggingface": "microsoft/DialoGPT-medium",
}
class AICredentialService:
    def __init__(self, db: Session):
        self.db = db

    def create_credential(self, user_id: int, provider: str, api_key: str, model_name: str | None = None, set_default: bool = False) -> AICredential:
        # Encrypt key
        token = encrypt(api_key)
        provider = provider.lower()
        if(not model_name or model_name == "default"):
            model_name = DEFAULT_MODELS.get(provider)
        if set_default:
            # unset other defaults for this user
            self.db.query(AICredential).filter(AICredential.user_id == user_id).update({"is_default": False})
        cred = AICredential(
            user_id=user_id,
            provider=provider,
            encrypted_key=token,
            model_name=model_name,
            is_default=set_default,
            created_at=datetime.utcnow().isoformat(),
        )
        self.db.add(cred)
        self.db.commit()
        self.db.refresh(cred)
        return cred

    def get_default_credential(self, user_id: int) -> AICredential | None:
        cred = (
        self.db.query(AICredential)
        .filter(
            AICredential.user_id == user_id,
            AICredential.is_default == True,
        )
        .first()
        )

        if cred: return cred

        return (
        self.db.query(AICredential)
        .filter(AICredential.user_id == user_id)
        .first()
       )

    def list_credentials(self, user_id: int) -> list[AICredential]:
        return self.db.query(AICredential).filter(AICredential.user_id == user_id).all()

    def delete_credential(self, user_id: int, credential_id: int) -> bool:
        cred = self.db.query(AICredential).filter(AICredential.user_id == user_id, AICredential.id == credential_id).first()
        if not cred:
            return False
        self.db.delete(cred)
        self.db.commit()
        return True

    def decrypt_key(self, credential: AICredential) -> str:
        return decrypt(credential.encrypted_key)
