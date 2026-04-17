from __future__ import annotations

from app.common.application.base_query import BaseQuery


class ListBlogsQuery(BaseQuery):
    """CQRS query to list blog posts for a user with pagination."""

    user_id: str
    limit: int = 20
    offset: int = 0
