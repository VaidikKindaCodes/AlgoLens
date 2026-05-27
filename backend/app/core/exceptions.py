from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code or "ERROR"


class ValidationError(AppException):
    def __init__(self, detail: str):
        super().__init__(detail, status.HTTP_422_UNPROCESSABLE_ENTITY, "VALIDATION_ERROR")


class NotFoundError(AppException):
    def __init__(self, detail: str):
        super().__init__(detail, status.HTTP_404_NOT_FOUND, "NOT_FOUND")


class UnauthorizedError(AppException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail, status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED")


class ForbiddenError(AppException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(detail, status.HTTP_403_FORBIDDEN, "FORBIDDEN")


class ConflictError(AppException):
    def __init__(self, detail: str):
        super().__init__(detail, status.HTTP_409_CONFLICT, "CONFLICT")


class RateLimitError(AppException):
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(detail, status.HTTP_429_TOO_MANY_REQUESTS, "RATE_LIMIT_EXCEEDED")


class ExternalServiceError(AppException):
    def __init__(self, detail: str = "External service error"):
        super().__init__(detail, status.HTTP_503_SERVICE_UNAVAILABLE, "SERVICE_ERROR")


class CodeExecutionError(AppException):
    def __init__(self, detail: str):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, "CODE_EXECUTION_ERROR")


class AIServiceError(AppException):
    def __init__(self, detail: str):
        super().__init__(detail, status.HTTP_503_SERVICE_UNAVAILABLE, "AI_SERVICE_ERROR")


class InvalidLanguageError(AppException):
    def __init__(self, language: str):
        super().__init__(
            f"Language '{language}' is not supported",
            status.HTTP_400_BAD_REQUEST,
            "INVALID_LANGUAGE",
        )


class WorkspaceNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("Workspace not found")


class UserNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("User not found")
