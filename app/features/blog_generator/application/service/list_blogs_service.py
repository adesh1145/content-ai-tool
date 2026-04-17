from __future__ import annotations

from app.common.port.inbound.use_case import UseCase
from app.features.blog_generator.application.mapper.blog_mapper import BlogMapper
from app.features.blog_generator.application.query.list_blogs_query import ListBlogsQuery
from app.features.blog_generator.application.result.blog_result import BlogResult
from app.features.blog_generator.application.validator.blog_validator import BlogValidator
from app.features.blog_generator.domain.port.outbound.blog_repository_port import IBlogRepository


class ListBlogsService(UseCase[ListBlogsQuery, list[BlogResult]]):
    """List blog posts for a given user with pagination."""

    def __init__(self, blog_repo: IBlogRepository) -> None:
        self._blog_repo = blog_repo

    async def execute(self, input_data: ListBlogsQuery) -> list[BlogResult]:
        BlogValidator.validate_list(input_data)

        blogs = await self._blog_repo.list_by_user(
            input_data.user_id, limit=input_data.limit, offset=input_data.offset
        )
        return BlogMapper.to_result_list(blogs)
