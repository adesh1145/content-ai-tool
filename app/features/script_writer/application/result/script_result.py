from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScriptResult:
    """Result returned by the generate-script use case."""

    script_id: str = ""
    script_format: str = ""
    topic: str = ""
    script_text: str = ""
    word_count: int = 0
    estimated_duration_seconds: int = 0
    tokens_used: int = 0
