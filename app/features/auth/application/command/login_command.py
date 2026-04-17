from __future__ import annotations

from pydantic import BaseModel


class LoginCommand(BaseModel):
    """Command to authenticate a user and obtain tokens."""

    email: str
    password: str
