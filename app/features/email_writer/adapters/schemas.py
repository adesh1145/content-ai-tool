"""
app/features/email_writer/adapters/schemas.py
"""

from __future__ import annotations
from pydantic import BaseModel, Field


class EmailRequest(BaseModel):
    email_type: str = Field(..., description="cold_email | newsletter | followup | welcome")
    recipient_name: str = Field("there", max_length=100)
    sender_company: str = Field(..., min_length=2, max_length=200)
    topic: str = Field(..., min_length=5, max_length=500)
    tone: str = Field("professional")
    language: str = Field("en")
    context: str = Field("", max_length=500, description="Additional context or notes")


class EmailResponse(BaseModel):
    email_id: str
    email_type: str
    subject: str
    body: str
    word_count: int
    tokens_used: int
