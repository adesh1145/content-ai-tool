from abc import ABC, abstractmethod
from typing import Any


class IProductGateway(ABC):
    @abstractmethod
    async def save(self, product_data: dict[str, Any]) -> dict[str, Any]:
        """Save a generated product description to the database."""
        pass


class IProductAIService(ABC):
    @abstractmethod
    async def generate(
        self,
        product_name: str,
        category: str,
        features: list[str],
        tone: str,
        target_audience: str,
        language: str,
        word_count: int = 150,
    ) -> dict:
        """Generate the product description."""
        pass
