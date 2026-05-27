from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.repository import BaseRepository
from app.models.workspace import Workspace


class WorkspaceRepository(BaseRepository[Workspace]):
    def __init__(self, db: Session):
        super().__init__(db, Workspace)

    def get_user_workspaces(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Workspace]:
        return self.db.execute(
            select(Workspace)
            .where(Workspace.user_id == user_id)
            .offset(skip)
            .limit(limit)
        ).scalars().all()

    def get_user_workspaces_count(self, user_id: int) -> int:
        return self.db.query(Workspace).filter(
            Workspace.user_id == user_id
        ).count()

    def get_user_workspace(self, user_id: int, workspace_id: int) -> Workspace | None:
        return self.db.execute(
            select(Workspace).where(
                Workspace.user_id == user_id,
                Workspace.id == workspace_id,
            )
        ).scalar()
