from __future__ import annotations

from pydantic import BaseModel


class BlogResult(BaseModel):
    """Application-level result DTO for a blog post."""

    blog_id: str = ""
    title: str = ""
    body: str = ""
    outline: list[str] = []
    seo: dict = {}
    tokens_used: int = 0
    status: str = ""
