from __future__ import annotations

from pydantic import BaseModel


class AdResult(BaseModel):
    """Result DTO returned by the generate-ad use case."""

    ad_id: str = ""
    platform: str = ""
    headline: str = ""
    primary_text: str = ""
    cta_text: str = ""
    variations: list[dict] = []
    tokens_used: int = 0
