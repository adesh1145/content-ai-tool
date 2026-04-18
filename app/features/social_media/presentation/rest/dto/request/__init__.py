from __future__ import annotations

from pydantic import BaseModel, Field


class GenerateSocialPostRequest(BaseModel):
    platform: str = Field(..., description="Target platform: linkedin, twitter, instagram")
    topic: str = Field(..., min_length=5, max_length=500)
    tone: str = Field(default="professional")
    language: str = Field(default="en")
    target_audience: str = Field(default="general")
