from __future__ import annotations

from app.common.port.inbound.use_case import UseCase
from app.features.blog_generator.application.query.get_blog_query import GetBlogQuery
from app.features.blog_generator.application.result.blog_result import BlogResult


class IGetBlog(UseCase[GetBlogQuery, BlogResult]):
    """Input port for retrieving a single blog post."""
    ...
