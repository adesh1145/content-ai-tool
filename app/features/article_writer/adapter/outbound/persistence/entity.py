from __future__ import annotations

from sqlalchemy import Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base_model import Base


class ArticleContentModel(Base):
    __tablename__ = "article_contents"
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    topic: Mapped[str] = mapped_column(String(500), nullable=False)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    outline_json: Mapped[str | None] = mapped_column(JSON, nullable=True)
    tone: Mapped[str] = mapped_column(String(50), nullable=False, default="professional")
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    target_audience: Mapped[str | None] = mapped_column(String(200), nullable=True)
    word_count_target: Mapped[int] = mapped_column(Integer, nullable=False, default=1500)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    tokens_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
