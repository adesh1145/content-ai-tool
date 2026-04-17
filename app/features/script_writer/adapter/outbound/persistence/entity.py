from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base_model import Base


class ScriptModel(Base):
    """SQLAlchemy model for the scripts table."""

    __tablename__ = "scripts"
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    format: Mapped[str] = mapped_column(String(30), nullable=False)
    topic: Mapped[str] = mapped_column(String(500), nullable=False)
    script_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    tone: Mapped[str] = mapped_column(String(30), nullable=False, default="professional")
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    target_audience: Mapped[str] = mapped_column(String(300), nullable=False, default="")
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estimated_duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    tokens_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
