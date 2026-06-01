from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.activity import ActivityListResponse, DashboardSummaryResponse
from app.schemas.workspace import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    WorkspaceCreateRequest,
    WorkspaceListResponse,
    WorkspaceResponse,
    WorkspaceUpdateRequest,
)
from app.services.activity import ActivityService
from app.services.workspace import WorkspaceService
from app.services.code_execution import CodeExecutionService

router = APIRouter(prefix="/workspace", tags=["Workspace"])


@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workspace(
    data: WorkspaceCreateRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> WorkspaceResponse:
    service = WorkspaceService(db)
    workspace = service.create_workspace(current_user.id, data)
    return workspace


@router.get(
    "",
    response_model=WorkspaceListResponse,
)
def list_workspaces(
    current_user: CurrentUser,
    db: DbSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> WorkspaceListResponse:
    service = WorkspaceService(db)
    workspaces, total = service.list_workspaces(current_user.id, skip, limit)
    return WorkspaceListResponse(
        items=workspaces,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
    )


@router.post(
    "/run",
    response_model=CodeExecutionResponse,
    status_code=status.HTTP_201_CREATED,
)
def run_code(
    data: CodeExecutionRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> CodeExecutionResponse:
    service = CodeExecutionService(db)
    execution = service.execute_code(current_user.id, None, data)
    return execution


@router.post(
    "/{workspace_id}/run",
    response_model=CodeExecutionResponse,
    status_code=status.HTTP_201_CREATED,
)
def run_workspace_code(
    workspace_id: int,
    data: CodeExecutionRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> CodeExecutionResponse:
    workspace_service = WorkspaceService(db)
    workspace_service.get_workspace(current_user.id, workspace_id)

    execution_service = CodeExecutionService(db)
    execution = execution_service.execute_code(current_user.id, workspace_id, data)
    return execution


@router.get(
    "/history",
    response_model=ActivityListResponse,
)
def get_workspace_history(
    current_user: CurrentUser,
    db: DbSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None, min_length=1),
    type: str | None = Query(None, min_length=1),
) -> ActivityListResponse:
    service = ActivityService(db)
    return service.list_activity(current_user.id, skip=skip, limit=limit, search=search, activity_type=type)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
)
def get_workspace_summary(
    current_user: CurrentUser,
    db: DbSession,
) -> DashboardSummaryResponse:
    service = ActivityService(db)
    return service.get_dashboard_summary(current_user.id)


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def get_workspace(
    workspace_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> WorkspaceResponse:
    service = WorkspaceService(db)
    workspace = service.get_workspace(current_user.id, workspace_id)
    return workspace


@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def update_workspace(
    workspace_id: int,
    data: WorkspaceUpdateRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> WorkspaceResponse:
    service = WorkspaceService(db)
    workspace = service.update_workspace(current_user.id, workspace_id, data)
    return workspace


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_workspace(
    workspace_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    service = WorkspaceService(db)
    service.delete_workspace(current_user.id, workspace_id)
