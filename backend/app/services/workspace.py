from sqlalchemy.orm import Session

from app.core.exceptions import WorkspaceNotFoundError
from app.db.repositories import WorkspaceRepository
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreateRequest, WorkspaceUpdateRequest


class WorkspaceService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = WorkspaceRepository(db)

    def create_workspace(
        self, user_id: int, data: WorkspaceCreateRequest
    ) -> Workspace:
        workspace_dict = {
            "user_id": user_id,
            "title": data.title,
            "language": data.language.lower(),
            "code": data.code or "",
            "custom_input": data.custom_input or "",
        }
        return self.repository.create(workspace_dict)

    def get_workspace(self, user_id: int, workspace_id: int) -> Workspace:
        workspace = self.repository.get_user_workspace(user_id, workspace_id)
        if not workspace:
            raise WorkspaceNotFoundError()
        return workspace

    def list_workspaces(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[Workspace], int]:
        workspaces = self.repository.get_user_workspaces(user_id, skip, limit)
        total = self.repository.get_user_workspaces_count(user_id)
        return workspaces, total

    def update_workspace(
        self, user_id: int, workspace_id: int, data: WorkspaceUpdateRequest
    ) -> Workspace:
        workspace = self.get_workspace(user_id, workspace_id)
        update_dict = {}
        if data.title is not None:
            update_dict["title"] = data.title
        if data.code is not None:
            update_dict["code"] = data.code
        if data.custom_input is not None:
            update_dict["custom_input"] = data.custom_input

        if update_dict:
            for key, value in update_dict.items():
                setattr(workspace, key, value)
            self.db.commit()
            self.db.refresh(workspace)

        return workspace

    def delete_workspace(self, user_id: int, workspace_id: int) -> bool:
        workspace = self.get_workspace(user_id, workspace_id)
        self.db.delete(workspace)
        self.db.commit()
        return True
