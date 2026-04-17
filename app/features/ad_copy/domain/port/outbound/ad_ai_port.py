from __future__ import annotations

from abc import ABC, abstractmethod


class AdAIPort(ABC):
    """Output port: AI service that generates ad copy variations."""

    @abstractmethod
    async def generate(
        self,
        platform: str,
        product_name: str,
        product_description: str,
        target_audience: str,
        tone: str,
        language: str,
        num_variations: int = 2,
    ) -> dict:
        """
        Generate ad copy with variations.

        Returns a dict with keys: headline, primary_text, cta_text, variations, tokens_used.
        """
        ...
