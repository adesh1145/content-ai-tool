from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base_model import Base


class ScriptModel(Base):
    __tablename__ = "scripts"

    user_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    format: Mapped[str] = mapped_column(String(50), nullable=False)
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    script_text: Mapped[str] = mapped_column(Text, nullable=False)
    estimated_duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="completed")
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
