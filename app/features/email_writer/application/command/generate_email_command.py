from __future__ import annotations

from app.common.application.base_command import BaseCommand


class GenerateEmailCommand(BaseCommand):
    """Command to generate email content."""

    user_id: str = ""
    email_type: str = "cold_email"
    recipient_name: str = ""
    company_name: str = ""
    purpose: str = ""
    tone: str = "professional"
    language: str = "en"
    key_points: list[str] = []
