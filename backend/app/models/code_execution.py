from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.user import utc_now

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.workspace import Workspace


class CodeExecution(Base):
    __tablename__ = "code_executions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    workspace_id: Mapped[int | None] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"), index=True, nullable=True
    )
    language: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    custom_input: Mapped[str] = mapped_column(Text, nullable=True)
    output: Mapped[str] = mapped_column(Text, nullable=True)
    error: Mapped[str] = mapped_column(Text, nullable=True)
    execution_time_ms: Mapped[float | None] = mapped_column(nullable=True)
    memory_usage_bytes: Mapped[int | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending", index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False, index=True
    )

    user: Mapped["User"] = relationship(back_populates="code_executions")
    workspace: Mapped["Workspace | None"] = relationship()
