from __future__ import annotations

from pydantic import BaseModel


class UserResult(BaseModel):
    """Application-layer result returned after user creation or profile lookup."""

    user_id: str
    email: str
    full_name: str
    plan: str = "free"
    is_active: bool = True
