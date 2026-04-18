from __future__ import annotations

from pydantic import BaseModel


class ScriptGenerateResponse(BaseModel):
    """Outgoing response schema for a generated script."""

    script_id: str
    script_format: str
    topic: str
    script_text: str
    word_count: int
    estimated_duration_seconds: int
    tokens_used: int
