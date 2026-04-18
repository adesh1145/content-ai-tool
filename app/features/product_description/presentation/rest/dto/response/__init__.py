from __future__ import annotations

from pydantic import BaseModel


class GenerateProductResponse(BaseModel):
    """Outgoing response schema for generated product description."""

    product_id: str
    description: str
    word_count: int
    tokens_used: int
