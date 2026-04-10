"""
app/features/blog_generator/adapters/schemas.py
"""

from __future__ import annotations
from pydantic import BaseModel, Field


class BlogGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=10, max_length=500)
    tone: str = Field("professional", description="professional|casual|persuasive|educational")
    language: str = Field("en", description="Language code: en|hi|es|fr")
    target_audience: str = Field("general", max_length=100)
    focus_keyword: str = Field("", max_length=100)
    secondary_keywords: list[str] = Field(default_factory=list, max_length=10)
    word_count: int = Field(800, ge=300, le=5000)
    project_id: str | None = None


class SEOMetaResponse(BaseModel):
    meta_title: str
    meta_description: str
    slug: str
    focus_keyword: str
    readability_score: float
    word_count: int
    reading_time_minutes: int = 0


class BlogGenerateResponse(BaseModel):
    blog_id: str
    title: str
    body: str
    outline: list[str]
    seo: SEOMetaResponse
    tokens_used: int
    status: str
