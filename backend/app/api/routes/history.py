from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.problem import AISessionResponse, HistoryListResponse
from app.services.problem import ProblemService

router = APIRouter(prefix="/history", tags=["History"])


@router.get(
    "",
    response_model=HistoryListResponse,
)
def get_history(
    current_user: CurrentUser,
    db: DbSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
) -> HistoryListResponse:
    service = ProblemService(db)
    sessions, total = service.get_ai_sessions(current_user.id, skip, limit)
    return HistoryListResponse(
        items=sessions,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
    )


@router.get(
    "/{session_id}",
    response_model=AISessionResponse,
)
def get_history_item(
    session_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> AISessionResponse:
    service = ProblemService(db)
    session = service.get_ai_session(current_user.id, session_id)
    return session


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_history_item(
    session_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    service = ProblemService(db)
    service.delete_ai_session(current_user.id, session_id)
