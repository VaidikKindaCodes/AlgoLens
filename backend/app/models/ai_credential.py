from datetime import datetime, timezone
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


def utc_now() -> datetime:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc)


class AICredential(Base):
    __tablename__ = "ai_credentials"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    encrypted_key: Mapped[str] = mapped_column(String(1024), nullable=False)
    model_name: Mapped[str] = mapped_column(String(128), nullable=True)
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        String(64), default=lambda: utc_now().isoformat(), nullable=False
    )
