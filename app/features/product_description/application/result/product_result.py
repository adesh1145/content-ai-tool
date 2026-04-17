from __future__ import annotations

from pydantic import BaseModel


class ProductResult(BaseModel):
    """Result DTO returned by the generate-product-description use case."""

    product_id: str = ""
    description: str = ""
    word_count: int = 0
    tokens_used: int = 0
