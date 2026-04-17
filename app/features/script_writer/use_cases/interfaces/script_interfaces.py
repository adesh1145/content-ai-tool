from abc import ABC, abstractmethod
from typing import Any


class IScriptGateway(ABC):
    @abstractmethod
    async def save(self, script_data: dict[str, Any]) -> dict[str, Any]:
        """Save a generated script to the database."""
        pass


class IScriptAIService(ABC):
    @abstractmethod
    async def generate(
        self,
        format: str,
        topic: str,
        tone: str,
        target_audience: str,
        language: str,
        target_duration: int,
    ) -> dict[str, Any]:
        """Generate the script content."""
        pass
