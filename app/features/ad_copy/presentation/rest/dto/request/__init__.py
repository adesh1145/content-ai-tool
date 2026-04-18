from __future__ import annotations

from pydantic import BaseModel, Field


class GenerateAdRequest(BaseModel):
    """Incoming request schema for ad copy generation."""

    platform: str = Field(..., description="Ad platform: 'google' or 'facebook'")
    product_name: str = Field(..., min_length=3, max_length=200)
    product_description: str = Field(..., min_length=10, max_length=500)
    target_audience: str = Field(..., max_length=200)
    tone: str = Field("persuasive")
    language: str = Field("en")
    num_variations: int = Field(2, ge=1, le=5)
