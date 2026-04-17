from __future__ import annotations

from app.common.application.base_command import BaseCommand


class GenerateProductCommand(BaseCommand):
    """Command to generate a product description."""

    user_id: str = ""
    product_name: str = ""
    category: str = ""
    features: list[str] = []
    tone: str = "professional"
    target_audience: str = ""
    language: str = "en"
    word_count: int = 200
