"""
app/features/ad_copy/adapters/schemas.py + app/features/ad_copy/drivers/routes.py
"""

from __future__ import annotations
from pydantic import BaseModel, Field


class AdCopyRequest(BaseModel):
    platform: str = Field(..., description="google | facebook")
    product_or_service: str = Field(..., min_length=3, max_length=200)
    target_audience: str = Field(..., max_length=200)
    unique_selling_point: str = Field("", max_length=300)
    tone: str = Field("persuasive")
    num_variations: int = Field(3, ge=1, le=5)


class AdVariationResponse(BaseModel):
    headline: str
    body: str
    cta: str


class AdCopyResponse(BaseModel):
    ad_id: str
    platform: str
    variations: list[AdVariationResponse]
    tokens_used: int
