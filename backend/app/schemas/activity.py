from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ActivityItem(BaseModel):
    id: str
    type: str
    title: str
    summary: str | None = None
    language: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ActivityListResponse(BaseModel):
    items: list[ActivityItem]
    total: int
    page: int
    page_size: int
    total_pages: int


class DashboardSummaryResponse(BaseModel):
    problems_analyzed: int
    ai_sessions: int
    code_runs: int
    saved_workspaces: int
    recent_history: list[ActivityItem]
