"""
app/features/social_media/adapters/schemas.py
"""

from __future__ import annotations
from pydantic import BaseModel, Field


class SocialPostRequest(BaseModel):
    topic: str = Field(..., min_length=5, max_length=500)
    platform: str = Field(..., description="linkedin | twitter | instagram")
    tone: str = Field("professional", description="professional|casual|inspirational|humorous")
    language: str = Field("en")
    target_audience: str = Field("general", max_length=100)
    include_emoji: bool = True


class SocialPostResponse(BaseModel):
    post_id: str
    platform: str
    caption: str
    hashtags: list[str]
    char_count: int
    within_limit: bool
    tokens_used: int
