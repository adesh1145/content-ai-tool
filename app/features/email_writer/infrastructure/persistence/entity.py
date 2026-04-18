from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base_model import Base


class EmailContentModel(Base):
    """SQLAlchemy model for the email_contents table."""

    __tablename__ = "email_contents"
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    email_type: Mapped[str] = mapped_column(String(50), nullable=False)
    recipient_name: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    company_name: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    purpose: Mapped[str] = mapped_column(Text, nullable=False, default="")
    subject_line: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    tone: Mapped[str] = mapped_column(String(30), nullable=False, default="professional")
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    tokens_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
