from __future__ import annotations

from pydantic import BaseModel, Field


class GenerateEmailRequest(BaseModel):
    """Incoming request schema for email content generation."""

    email_type: str = Field(
        ..., description="Email type: 'cold_email', 'newsletter', 'followup', or 'welcome'"
    )
    recipient_name: str = Field(..., min_length=1, max_length=200)
    company_name: str = Field("", max_length=200)
    purpose: str = Field(..., min_length=10, max_length=500)
    tone: str = Field("professional")
    language: str = Field("en")
    key_points: list[str] = Field(default_factory=list)
