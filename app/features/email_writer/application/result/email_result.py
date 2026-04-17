from __future__ import annotations

from pydantic import BaseModel


class EmailResult(BaseModel):
    """Result DTO returned by the generate-email use case."""

    email_id: str = ""
    email_type: str = ""
    subject_line: str = ""
    body: str = ""
    tokens_used: int = 0
