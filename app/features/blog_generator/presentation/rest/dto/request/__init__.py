from __future__ import annotations

from pydantic import BaseModel, Field


class BlogGenerateRequest(BaseModel):
    """Pydantic schema for the blog generation endpoint."""

    topic: str = Field(..., min_length=10, max_length=500)
    tone: str = Field("professional", description="professional|casual|educational|persuasive|formal|friendly")
    language: str = Field("en", description="Language code: en|hi|es|fr|de|pt")
    target_audience: str = Field("general", max_length=200)
    focus_keyword: str = Field("", max_length=100)
    secondary_keywords: list[str] = Field(default_factory=list, max_length=10)
    word_count: int = Field(800, ge=300, le=5000)
    project_id: str | None = Field(None, max_length=36)
