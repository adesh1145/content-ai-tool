"""
app/features/product_description/adapters/schemas.py
"""

from __future__ import annotations
from pydantic import BaseModel, Field


class ProductDescRequest(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=200)
    category: str = Field(..., max_length=100, description="e.g. Electronics, Clothing, Food")
    features: list[str] = Field(..., min_length=1, max_length=20)
    tone: str = Field("professional", description="professional|casual|persuasive|friendly")
    target_audience: str = Field("general shoppers", max_length=150)
    language: str = Field("en")
    word_count: int = Field(150, ge=50, le=500)


class ProductDescResponse(BaseModel):
    product_id: str
    product_name: str
    description: str
    word_count: int
    tokens_used: int
