from __future__ import annotations

from pydantic import BaseModel, Field


class SEOAnalyzeRequest(BaseModel):
    """Incoming request schema for SEO analysis."""

    content: str = Field(..., min_length=100, description="Content to analyze (markdown or plain text)")
    focus_keyword: str = Field("", max_length=100)
    meta_title: str = Field("", max_length=70)
    meta_description: str = Field("", max_length=200)
    url: str = Field("", max_length=500)


class MetaGenerateRequest(BaseModel):
    """Incoming request schema for meta tag generation."""

    content: str = Field(..., min_length=100, description="Content to generate meta tags for")
    focus_keyword: str = Field("", max_length=100)
