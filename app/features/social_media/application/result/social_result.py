from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SocialResult:
    post_id: str
    platform: str
    content: str
    hashtags: list[str] = field(default_factory=list)
    tokens_used: int = 0
    status: str = "pending"
