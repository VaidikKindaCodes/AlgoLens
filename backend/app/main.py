from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.api.routes import auth_router, problems_router, workspace_router, history_router, ai_credentials_router
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.database import Base, engine
from app.models import ai_credential  # noqa: F401

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.ENVIRONMENT == "development" else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _ensure_user_ai_columns() -> None:
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    existing = {column["name"] for column in inspector.get_columns("users")}
    statements = []
    if "ai_provider" not in existing:
        statements.append("ALTER TABLE users ADD COLUMN ai_provider VARCHAR(64)")
    if "ai_encrypted_key" not in existing:
        statements.append("ALTER TABLE users ADD COLUMN ai_encrypted_key VARCHAR(1024)")
    if "ai_model_name" not in existing:
        statements.append("ALTER TABLE users ADD COLUMN ai_model_name VARCHAR(128)")

    if not statements:
        return

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    _ensure_user_ai_columns()
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        lifespan=lifespan,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    prefix = settings.API_V1_PREFIX
    application.include_router(auth_router, prefix=prefix)
    application.include_router(problems_router, prefix=prefix)
    application.include_router(workspace_router, prefix=prefix)
    application.include_router(history_router, prefix=prefix)
    application.include_router(ai_credentials_router, prefix=prefix)

    @application.get("/", tags=["System"])
    def root() -> dict[str, str]:
        return {"message": "AlgoLens Backend Running"}

    @application.get("/health", tags=["System"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()
