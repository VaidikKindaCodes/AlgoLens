from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.user import utc_now

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.workspace import Workspace


class AISession(Base):
    __tablename__ = "ai_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    workspace_id: Mapped[int | None] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"), index=True, nullable=True
    )
    action_type: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True
    )
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    model_used: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False, index=True
    )

    user: Mapped["User"] = relationship(back_populates="ai_sessions")
    workspace: Mapped["Workspace | None"] = relationship()
