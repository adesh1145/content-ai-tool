"""
app/features/blog_generator/entities/blog_content.py
─────────────────────────────────────────────────────────────
BlogContent domain entity.
Layer 1: Enterprise Business Rules — zero external deps.

Includes full SEO fields as first-class domain properties.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.entities.base_entity import BaseEntity
from app.core.entities.value_objects import GenerationStatus, Language, Tone


@dataclass
class SEOMetadata:
    """SEO metadata for blog content — all fields are domain-level."""
    meta_title: str = ""          # 50–60 chars
    meta_description: str = ""   # 150–160 chars
    slug: str = ""                # URL-friendly slug
    focus_keyword: str = ""
    secondary_keywords: list[str] = field(default_factory=list)
    canonical_url: str = ""
    schema_markup: str = ""       # JSON-LD schema string
    reading_time_minutes: int = 0
    word_count: int = 0
    readability_score: float = 0.0   # Flesch-Kincaid score


@dataclass
class BlogContent(BaseEntity):
    user_id: str = ""
    project_id: str | None = None

    # Content
    topic: str = ""
    title: str = ""
    outline: list[str] = field(default_factory=list)  # Section headings
    body: str = ""                 # Full markdown body
    tone: Tone = Tone.PROFESSIONAL
    language: Language = Language.ENGLISH
    target_audience: str = ""

    # SEO (first-class — not an afterthought)
    seo: SEOMetadata = field(default_factory=SEOMetadata)

    # Status
    status: GenerationStatus = GenerationStatus.PENDING
    tokens_used: int = 0
    error_message: str | None = None

    def mark_completed(self, body: str, seo: SEOMetadata, tokens: int) -> None:
        self.body = body
        self.seo = seo
        self.tokens_used = tokens
        self.status = GenerationStatus.COMPLETED
        self.touch()

    def mark_failed(self, reason: str) -> None:
        self.status = GenerationStatus.FAILED
        self.error_message = reason
        self.touch()
