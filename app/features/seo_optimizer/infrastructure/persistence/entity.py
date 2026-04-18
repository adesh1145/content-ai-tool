from __future__ import annotations

from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base_model import Base


class SEOAnalysisModel(Base):
    """SQLAlchemy model for the seo_analyses table."""

    __tablename__ = "seo_analyses"
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    content_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    focus_keyword: Mapped[str] = mapped_column(String(100), nullable=False, default="")

    overall_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    readability_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    flesch_reading_ease: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    flesch_kincaid_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    avg_sentence_length: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    word_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    heading_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    has_h1: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    internal_links_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    external_links_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    image_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    images_with_alt: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    has_meta_title: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_meta_description: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    meta_title_length: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    meta_description_length: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    keyword_density_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    suggestions_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    tokens_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
