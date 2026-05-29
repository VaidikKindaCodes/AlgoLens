from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProblemAnalyzeRequest(BaseModel):
    problem_statement: str = Field(min_length=10, max_length=50000)


class ProblemHintsRequest(BaseModel):
    problem_statement: str = Field(min_length=10, max_length=50000)
    level: int = Field(ge=1, le=3, description="1: Beginner, 2: Intermediate, 3: Advanced")


class ProblemSolutionRequest(BaseModel):
    problem_statement: str = Field(min_length=10, max_length=50000)
    language: str = Field(min_length=1, max_length=32)


class ProblemTestCasesRequest(BaseModel):
    problem_statement: str = Field(min_length=10, max_length=50000)
    count: int = Field(ge=1, le=100, description="Number of test cases to generate")


class CodeReviewRequest(BaseModel):
    problem_statement: str = Field(min_length=10, max_length=50000)
    code: str = Field(min_length=1, max_length=10000)
    language: str = Field(min_length=1, max_length=32)


class StressTestRequest(BaseModel):
    problem_statement: str = Field(min_length=10, max_length=50000)
    solution_code: str = Field(min_length=1, max_length=10000)
    brute_force_code: str = Field(min_length=1, max_length=10000)
    language: str = Field(min_length=1, max_length=32)
    test_count: int = Field(ge=1, le=1000)


class AIResponse(BaseModel):
    content: str
    model_used: str
    timestamp: datetime


class ProblemAnalysisResponse(BaseModel):
    id: int
    user_id: int
    problem_statement: str
    response: str = Field(alias="content")
    model_used: str = Field(alias="model")
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, by_alias=True)


class AISessionResponse(BaseModel):
    id: int
    user_id: int
    workspace_id: int | None
    action_type: str = Field(alias="type")
    prompt: str
    response: str = Field(alias="content")
    model_used: str = Field(alias="model")
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, by_alias=True)


class HistoryListResponse(BaseModel):
    items: list[AISessionResponse]
    total: int
    page: int
    page_size: int
