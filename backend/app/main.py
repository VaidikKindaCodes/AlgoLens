from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
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
    application.include_router(auth_router, prefix=settings.API_V1_PREFIX)

    @application.get("/", tags=["System"])
    def root() -> dict[str, str]:
        return {"message": "AlgoLens Backend Running"}

    @application.get("/health", tags=["System"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()
