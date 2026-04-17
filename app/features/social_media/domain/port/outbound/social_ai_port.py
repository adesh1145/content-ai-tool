from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SocialAIResult:
    content: str = ""
    hashtags: list[str] = field(default_factory=list)
    char_count: int = 0


class ISocialAIService(ABC):
    @abstractmethod
    async def generate(
        self,
        *,
        topic: str,
        platform: str,
        tone: str,
        language: str,
        target_audience: str,
    ) -> SocialAIResult: ...
