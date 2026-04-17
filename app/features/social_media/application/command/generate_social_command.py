from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GenerateSocialCommand:
    user_id: str
    platform: str
    topic: str
    tone: str = "professional"
    language: str = "en"
    target_audience: str = "general"
