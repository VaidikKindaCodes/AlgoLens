from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
