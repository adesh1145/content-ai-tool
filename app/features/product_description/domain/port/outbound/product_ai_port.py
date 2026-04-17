from __future__ import annotations

from abc import ABC, abstractmethod


class ProductAIPort(ABC):
    """Output port: AI service that generates product descriptions."""

    @abstractmethod
    async def generate(
        self,
        product_name: str,
        category: str,
        features: list[str],
        tone: str,
        target_audience: str,
        language: str,
        word_count: int,
    ) -> dict:
        """
        Generate a product description using the F-A-B framework.

        Returns a dict with keys: description, tokens_used.
        """
        ...
