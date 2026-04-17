from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GenerateScriptCommand:
    """Command to generate a script for a given format and topic."""

    user_id: str = ""
    script_format: str = ""
    topic: str = ""
    tone: str = "professional"
    language: str = "en"
    target_audience: str = ""
    duration_seconds: int = 0
