from __future__ import annotations

from abc import ABC, abstractmethod


class EmailAIPort(ABC):
    """Output port: AI service that generates email content."""

    @abstractmethod
    async def generate(
        self,
        email_type: str,
        recipient_name: str,
        company_name: str,
        purpose: str,
        tone: str,
        language: str,
        key_points: list[str] | None = None,
    ) -> dict:
        """
        Generate email content with type-specific prompts.

        Returns a dict with keys: subject_line, body, tokens_used.
        """
        ...
