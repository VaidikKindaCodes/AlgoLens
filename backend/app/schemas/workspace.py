from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkspaceCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    language: str = Field(min_length=1, max_length=32)
    code: str | None = None
    custom_input: str | None = None


class WorkspaceUpdateRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    code: str | None = None
    custom_input: str | None = None


class WorkspaceResponse(BaseModel):
    id: int
    user_id: int
    title: str
    language: str
    code: str | None
    custom_input: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkspaceListResponse(BaseModel):
    items: list[WorkspaceResponse]
    total: int
    page: int
    page_size: int


class CodeExecutionRequest(BaseModel):
    language: str = Field(min_length=1, max_length=32)
    code: str = Field(min_length=1, max_length=10000)
    custom_input: str | None = None


class CodeExecutionResponse(BaseModel):
    id: int
    language: str
    code: str
    custom_input: str | None
    output: str | None
    error: str | None
    execution_time_ms: float | None
    memory_usage_bytes: int | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
