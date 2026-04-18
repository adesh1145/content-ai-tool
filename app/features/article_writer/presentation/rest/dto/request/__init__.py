from __future__ import annotations

from pydantic import BaseModel, Field


class GenerateArticleRequest(BaseModel):
    topic: str = Field(..., min_length=10, max_length=500)
    tone: str = Field(default="professional")
    language: str = Field(default="en")
    target_audience: str = Field(default="general")
    focus_keyword: str = Field(default="")
    word_count_target: int = Field(default=1500, ge=500, le=5000)
