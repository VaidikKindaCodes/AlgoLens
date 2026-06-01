from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.problem import (
    CodeReviewRequest,
    ProblemAnalyzeRequest,
    ProblemAnalysisResponse,
    ProblemHintsRequest,
    ProblemSolutionRequest,
    ProblemTestCasesRequest,
    AISessionResponse,
    AIResponse,
)
from app.services.problem import ProblemService

router = APIRouter(prefix="/problems", tags=["Problems"])


@router.post(
    "/analyze",
    response_model=ProblemAnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
def analyze_problem(
    data: ProblemAnalyzeRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> ProblemAnalysisResponse:
    service = ProblemService(db)
    analysis = service.analyze_problem(current_user.id, data)
    return analysis


@router.post(
    "/hints",
    response_model=AISessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_hints(
    data: ProblemHintsRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> AISessionResponse:
    service = ProblemService(db)
    session = service.generate_hints(current_user.id, None, data)
    return session


@router.post(
    "/solution",
    response_model=AISessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_solution(
    data: ProblemSolutionRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> AISessionResponse:
    service = ProblemService(db)
    session = service.generate_solution(current_user.id, None, data)
    return session


@router.post(
    "/testcases",
    response_model=AISessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_testcases(
    data: ProblemTestCasesRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> AISessionResponse:
    service = ProblemService(db)
    session = service.generate_testcases(current_user.id, None, data)
    return session


@router.post(
    "/review",
    response_model=AISessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def review_code(
    data: CodeReviewRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> AISessionResponse:
    service = ProblemService(db)
    session = service.review_code(current_user.id, None, data)
    return session
