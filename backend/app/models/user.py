from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.refresh_token import RefreshToken
    from app.models.workspace import Workspace
    from app.models.problem_analysis import ProblemAnalysis
    from app.models.ai_session import AISession
    from app.models.code_execution import CodeExecution


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    # Default AI credential saved on user schema for quick access
    ai_provider: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ai_encrypted_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    ai_model_name: Mapped[str | None] = mapped_column(String(128), nullable=True)

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    workspaces: Mapped[list["Workspace"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    problem_analyses: Mapped[list["ProblemAnalysis"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    ai_sessions: Mapped[list["AISession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    code_executions: Mapped[list["CodeExecution"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
