from abc import ABC, abstractmethod
from typing import Any


class IEmailGateway(ABC):
    @abstractmethod
    async def save(self, email_data: dict[str, Any]) -> dict[str, Any]:
        """Save a generated email to the database."""
        pass


class IEmailAIService(ABC):
    @abstractmethod
    async def generate(
        self,
        email_type: str,
        recipient_name: str,
        sender_company: str,
        topic: str,
        tone: str,
        language: str,
        context: str = "",
    ) -> dict[str, Any]:
        """Generate the email content."""
        pass
