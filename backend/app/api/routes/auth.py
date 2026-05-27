from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.auth import (
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth import (
    authenticate_user,
    issue_token_pair,
    register_user,
    revoke_all_user_tokens,
    revoke_refresh_token,
    rotate_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(data: RegisterRequest, db: DbSession) -> UserResponse:
    return register_user(db, data)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: DbSession) -> TokenResponse:
    user = authenticate_user(db, data)
    return issue_token_pair(db, user)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: DbSession) -> TokenResponse:
    return rotate_refresh_token(db, data.refresh_token)


@router.post("/logout", response_model=MessageResponse)
def logout(data: RefreshRequest, db: DbSession) -> MessageResponse:
    revoke_refresh_token(db, data.refresh_token)
    return MessageResponse(message="Logged out successfully")


@router.post("/logout-all", response_model=MessageResponse)
def logout_all(current_user: CurrentUser, db: DbSession) -> MessageResponse:
    revoke_all_user_tokens(db, current_user.id)
    return MessageResponse(message="Logged out from all sessions")


@router.get("/me", response_model=UserResponse)
def me(current_user: CurrentUser) -> UserResponse:
    return current_user
