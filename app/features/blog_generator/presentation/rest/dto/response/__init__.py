from __future__ import annotations

from pydantic import BaseModel


class SEOMetaResponse(BaseModel):
    """Pydantic schema for SEO metadata in API responses."""

    meta_title: str = ""
    meta_description: str = ""
    slug: str = ""
    focus_keyword: str = ""
    secondary_keywords: list[str] = []
    word_count: int = 0
    readability_score: float = 0.0
    reading_time_minutes: int = 0


class BlogGenerateResponse(BaseModel):
    """Pydantic schema for the full blog API response."""

    blog_id: str
    title: str = ""
    body: str = ""
    outline: list[str] = []
    seo: SEOMetaResponse = SEOMetaResponse()
    tokens_used: int = 0
    status: str = ""
