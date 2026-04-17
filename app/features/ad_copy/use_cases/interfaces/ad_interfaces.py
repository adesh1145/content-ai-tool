from abc import ABC, abstractmethod
from typing import Any


class IAdGateway(ABC):
    @abstractmethod
    async def save(self, ad_data: dict[str, Any]) -> dict[str, Any]:
        """Save generated ad copy variations to the database."""
        pass


class IAdAIService(ABC):
    @abstractmethod
    async def generate(
        self,
        platform: str,
        product: str,
        target_audience: str,
        usp: str,
        tone: str,
        num_variations: int = 3,
    ) -> list[dict]:
        """Generate the ad copy variations."""
        pass
