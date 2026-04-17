from abc import ABC, abstractmethod
from typing import Any


class ISocialGateway(ABC):
    @abstractmethod
    async def save(self, post_data: dict[str, Any]) -> dict[str, Any]:
        """Save a generated social post to the database."""
        pass


class ISocialAIService(ABC):
    @abstractmethod
    async def generate(
        self,
        topic: str,
        platform: str,
        tone: str,
        language: str,
        target_audience: str,
        include_emoji: bool = True,
    ) -> dict[str, Any]:
        """Generate the social media post."""
        pass
