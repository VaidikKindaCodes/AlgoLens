from sqlalchemy import String, case, cast, func, literal, or_, select, union_all
from sqlalchemy.orm import Session

from app.models.ai_session import AISession
from app.models.code_execution import CodeExecution
from app.models.problem_analysis import ProblemAnalysis
from app.models.workspace import Workspace
from app.schemas.activity import ActivityItem, ActivityListResponse, DashboardSummaryResponse


AI_SESSION_TYPES = {
    "generate_hints": "hint",
    "generate_solution": "solution",
    "generate_testcases": "test_cases",
    "review_code": "review",
}

AI_SESSION_TITLES = {
    "generate_hints": "Generated hints",
    "generate_solution": "Generated solution",
    "generate_testcases": "Generated test cases",
    "review_code": "Reviewed code",
}


class ActivityService:
    def __init__(self, db: Session):
        self.db = db

    def _activity_query(self, user_id: int):
        workspace_items = select(
            cast(Workspace.id, String).label("id"),
            literal("workspace").label("type"),
            Workspace.title.label("title"),
            Workspace.language.label("summary"),
            Workspace.language.label("language"),
            Workspace.updated_at.label("created_at"),
        ).where(Workspace.user_id == user_id)

        execution_items = select(
            cast(CodeExecution.id, String).label("id"),
            literal("code_run").label("type"),
            literal("Code run").label("title"),
            CodeExecution.status.label("summary"),
            CodeExecution.language.label("language"),
            CodeExecution.created_at.label("created_at"),
        ).where(CodeExecution.user_id == user_id)

        analysis_items = select(
            cast(ProblemAnalysis.id, String).label("id"),
            literal("analysis").label("type"),
            literal("Problem analysis").label("title"),
            func.substr(ProblemAnalysis.problem_statement, 1, 120).label("summary"),
            cast(literal(None), String).label("language"),
            ProblemAnalysis.created_at.label("created_at"),
        ).where(ProblemAnalysis.user_id == user_id)

        ai_items = select(
            cast(AISession.id, String).label("id"),
            case(
                AI_SESSION_TYPES,
                value=AISession.action_type,
                else_="analysis",
            ).label("type"),
            case(
                AI_SESSION_TITLES,
                value=AISession.action_type,
                else_="AI session",
            ).label("title"),
            func.substr(AISession.prompt, 1, 120).label("summary"),
            cast(literal(None), String).label("language"),
            AISession.created_at.label("created_at"),
        ).where(AISession.user_id == user_id)

        return union_all(workspace_items, execution_items, analysis_items, ai_items).subquery()

    def list_activity(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
        search: str | None = None,
        activity_type: str | None = None,
    ) -> ActivityListResponse:
        query = self._activity_query(user_id)

        filters = []
        if activity_type and activity_type != "all":
            filters.append(query.c.type == activity_type)
        if search:
            pattern = f"%{search}%"
            filters.append(
                or_(
                    query.c.title.ilike(pattern),
                    func.coalesce(query.c.summary, "").ilike(pattern),
                    func.coalesce(query.c.language, "").ilike(pattern),
                )
            )

        base_select = select(
            query.c.id,
            query.c.type,
            query.c.title,
            query.c.summary,
            query.c.language,
            query.c.created_at,
        ).select_from(query)
        count_select = select(func.count()).select_from(query)

        if filters:
            base_select = base_select.where(*filters)
            count_select = count_select.where(*filters)

        ordered = base_select.order_by(query.c.created_at.desc(), query.c.id.desc())
        rows = self.db.execute(ordered.offset(skip).limit(limit)).all()
        total = self.db.execute(count_select).scalar_one()
        items = [
            ActivityItem(
                id=row.id,
                type=row.type,
                title=row.title,
                summary=row.summary,
                language=row.language,
                created_at=row.created_at,
            )
            for row in rows
        ]

        total_pages = (total + limit - 1) // limit if limit else 0
        page = skip // limit + 1 if limit else 1
        return ActivityListResponse(
            items=items,
            total=total,
            page=page,
            page_size=limit,
            total_pages=total_pages,
        )

    def get_dashboard_summary(self, user_id: int, recent_limit: int = 5) -> DashboardSummaryResponse:
        problems_analyzed = self.db.query(ProblemAnalysis).filter(ProblemAnalysis.user_id == user_id).count()
        ai_sessions = self.db.query(AISession).filter(AISession.user_id == user_id).count()
        code_runs = self.db.query(CodeExecution).filter(CodeExecution.user_id == user_id).count()
        saved_workspaces = self.db.query(Workspace).filter(Workspace.user_id == user_id).count()
        recent_history = self.list_activity(user_id, skip=0, limit=recent_limit).items

        return DashboardSummaryResponse(
            problems_analyzed=problems_analyzed,
            ai_sessions=ai_sessions,
            code_runs=code_runs,
            saved_workspaces=saved_workspaces,
            recent_history=recent_history,
        )
