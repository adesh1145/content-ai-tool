"""
app/features/script_writer/adapters/schemas.py
"""

from __future__ import annotations
from pydantic import BaseModel, Field


class ScriptRequest(BaseModel):
    script_format: str = Field(..., description="youtube | reel | podcast")
    topic: str = Field(..., min_length=5, max_length=500)
    tone: str = Field("educational")
    language: str = Field("en")
    target_audience: str = Field("general", max_length=150)
    duration_seconds: int = Field(300, ge=15, le=3600, description="Target video duration in seconds")


class ScriptResponse(BaseModel):
    script_id: str
    script_format: str
    topic: str
    script: str
    word_count: int
    estimated_duration_seconds: int
    tokens_used: int
