from __future__ import annotations

from app.common.application.base_query import BaseQuery


class GetBlogQuery(BaseQuery):
    """CQRS query to retrieve a single blog post by ID."""

    blog_id: str
    user_id: str = ""
