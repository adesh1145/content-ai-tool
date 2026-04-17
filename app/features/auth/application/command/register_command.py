from __future__ import annotations

from pydantic import BaseModel


class RegisterCommand(BaseModel):
    """Command to register a new user account."""

    email: str
    password: str
    full_name: str
