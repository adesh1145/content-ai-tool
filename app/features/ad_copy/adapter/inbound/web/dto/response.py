from __future__ import annotations

from pydantic import BaseModel


class AdVariationResponse(BaseModel):
    """Single ad variation in the response."""

    headline: str
    primary_text: str
    cta_text: str


class GenerateAdResponse(BaseModel):
    """Outgoing response schema for generated ad copy."""

    ad_id: str
    platform: str
    headline: str
    primary_text: str
    cta_text: str
    variations: list[dict]
    tokens_used: int
