from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base_model import Base


class AdCopyModel(Base):
    """SQLAlchemy model for the ad_copies table."""

    __tablename__ = "ad_copies"
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    product_description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    target_audience: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    headline: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    primary_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    cta_text: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    variations_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    tone: Mapped[str] = mapped_column(String(30), nullable=False, default="persuasive")
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    tokens_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
