from __future__ import annotations

from pydantic import BaseModel


class GenerateEmailResponse(BaseModel):
    """Outgoing response schema for generated email content."""

    email_id: str
    email_type: str
    subject_line: str
    body: str
    tokens_used: int
