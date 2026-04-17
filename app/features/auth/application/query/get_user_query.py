from __future__ import annotations

from pydantic import BaseModel


class GetUserQuery(BaseModel):
    """Query to retrieve user profile by ID."""

    user_id: str
