from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.auth import (
    GoogleAuthRequest,
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    ResendOtpRequest,
    TokenResponse,
    UrlResponse,
    UserResponse,
    VerifyOtpRequest,
)
from app.services.auth import (
    authenticate_google_user,
    authenticate_user,
    get_google_login_url,
    issue_token_pair,
    register_user,
    resend_otp,
    revoke_all_user_tokens,
    revoke_refresh_token,
    rotate_refresh_token,
    verify_otp,
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


@router.post("/verify-otp", response_model=TokenResponse)
def verify_email(data: VerifyOtpRequest, db: DbSession) -> TokenResponse:
    return verify_otp(db, data)


@router.post("/resend-otp", response_model=MessageResponse)
def resend_verification_code(data: ResendOtpRequest, db: DbSession) -> MessageResponse:
    resend_otp(db, data)
    return MessageResponse(message="Verification code resent")


@router.get("/google/url", response_model=UrlResponse)
def google_login_url() -> UrlResponse:
    return UrlResponse(url=get_google_login_url())


@router.post("/google", response_model=TokenResponse)
def google_login(data: GoogleAuthRequest, db: DbSession) -> TokenResponse:
    return authenticate_google_user(db, data.code)


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
