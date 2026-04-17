from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ScriptAIResult:
    """Result returned by the AI service after generating a script."""

    script_text: str = ""
    word_count: int = 0
    estimated_duration_seconds: int = 0


class IScriptAIService(ABC):
    """Output port: AI service that generates scripts."""

    @abstractmethod
    async def generate_script(
        self,
        *,
        script_format: str,
        topic: str,
        tone: str,
        language: str,
        target_audience: str,
        duration_seconds: int,
    ) -> ScriptAIResult: ...
