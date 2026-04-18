from __future__ import annotations

from pydantic import BaseModel


class SocialPostResponse(BaseModel):
    post_id: str
    platform: str
    content: str
    hashtags: list[str] = []
    tokens_used: int = 0
    status: str = "pending"
