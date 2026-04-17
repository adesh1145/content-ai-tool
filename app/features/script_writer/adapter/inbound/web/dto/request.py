from __future__ import annotations

from pydantic import BaseModel, Field


class ScriptGenerateRequest(BaseModel):
    """Incoming request schema for script generation."""

    script_format: str = Field(
        ..., description="Script format: 'youtube', 'reel', or 'podcast'"
    )
    topic: str = Field(..., min_length=3, max_length=500)
    tone: str = Field("professional")
    language: str = Field("en")
    target_audience: str = Field("", max_length=300)
    duration_seconds: int = Field(..., gt=0, description="Target duration in seconds")
