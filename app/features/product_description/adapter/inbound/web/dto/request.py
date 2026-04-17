from __future__ import annotations

from pydantic import BaseModel, Field


class GenerateProductRequest(BaseModel):
    """Incoming request schema for product description generation."""

    product_name: str = Field(..., min_length=3, max_length=200)
    category: str = Field("", max_length=100)
    features: list[str] = Field(..., min_length=1)
    tone: str = Field("professional")
    target_audience: str = Field("", max_length=200)
    language: str = Field("en")
    word_count: int = Field(200, ge=50, le=2000)
