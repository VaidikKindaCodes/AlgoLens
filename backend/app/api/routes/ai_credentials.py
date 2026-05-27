from fastapi import APIRouter, Depends, status, HTTPException
from app.api.dependencies import CurrentUser, DbSession
from app.services.ai_credentials import AICredentialService
from pydantic import BaseModel

router = APIRouter(prefix="/ai-credentials", tags=["AI Credentials"])


class CreateAICredentialRequest(BaseModel):
    provider: str
    api_key: str
    model_name: str | None = None
    set_default: bool | None = False


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_credential(data: CreateAICredentialRequest, current_user: CurrentUser, db: DbSession):
    service = AICredentialService(db)
    cred = service.create_credential(current_user.id, data.provider, data.api_key, data.model_name, bool(data.set_default))
    return {"id": cred.id, "provider": cred.provider, "model_name": cred.model_name, "is_default": cred.is_default}


@router.get("/", status_code=status.HTTP_200_OK)
def list_credentials(current_user: CurrentUser, db: DbSession):
    service = AICredentialService(db)
    creds = service.list_credentials(current_user.id)
    return [
        {"id": c.id, "provider": c.provider, "model_name": c.model_name, "is_default": c.is_default}
        for c in creds
    ]


@router.get("/default", status_code=status.HTTP_200_OK)
def get_default(current_user: CurrentUser, db: DbSession):
    service = AICredentialService(db)
    cred = service.get_default_credential(current_user.id)
    if not cred:
        raise HTTPException(status_code=404, detail="No default AI credential set")
    return {"id": cred.id, "provider": cred.provider, "model_name": cred.model_name, "is_default": cred.is_default}


@router.delete("/{credential_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_credential(credential_id: int, current_user: CurrentUser, db: DbSession):
    service = AICredentialService(db)
    ok = service.delete_credential(current_user.id, credential_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Credential not found")
    return {}
