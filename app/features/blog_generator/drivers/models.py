"""
app/features/blog_generator/drivers/models.py
─────────────────────────────────────────────────────────────
SQLAlchemy model for blog_contents table.
"""

from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base_model import Base


class BlogContentModel(Base):
    __tablename__ = "blog_contents"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    project_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    topic: Mapped[str] = mapped_column(String(500), nullable=False)
    title: Mapped[str | None] = mapped_column(String(300), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    outline_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    seo_json: Mapped[str | None] = mapped_column(Text, nullable=True)   # Serialised SEOMetadata
    tone: Mapped[str] = mapped_column(String(30), nullable=False, default="professional")
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    target_audience: Mapped[str | None] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    tokens_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
