
from app.api.routes.auth import router as auth_router
from app.api.routes.problems import router as problems_router
from app.api.routes.workspace import router as workspace_router
from app.api.routes.history import router as history_router
from app.api.routes.ai_credentials import router as ai_credentials_router

__all__ = ["auth_router", "problems_router", "workspace_router", "history_router", "ai_credentials_router"]
