"""
app/features/article_writer/adapters/schemas.py + drivers/routes.py
─────────────────────────────────────────────────────────────
Article writer schemas and routes.
"""

from __future__ import annotations
from pydantic import BaseModel, Field


class ArticleRequest(BaseModel):
    topic: str = Field(..., min_length=10, max_length=500)
    tone: str = Field("educational", description="professional|educational|casual|persuasive")
    language: str = Field("en")
    target_audience: str = Field("general", max_length=150)
    focus_keyword: str = Field("", max_length=100)
    word_count: int = Field(1500, ge=500, le=5000)
    project_id: str | None = None


class ArticleResponse(BaseModel):
    article_id: str
    topic: str
    final_article: str
    meta_title: str
    meta_description: str
    word_count: int
    tokens_used: int
    status: str
