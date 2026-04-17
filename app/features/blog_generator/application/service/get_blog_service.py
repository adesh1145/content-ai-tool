from __future__ import annotations

from app.common.exception.base_exception import NotFoundException
from app.common.port.inbound.use_case import UseCase
from app.features.blog_generator.application.mapper.blog_mapper import BlogMapper
from app.features.blog_generator.application.query.get_blog_query import GetBlogQuery
from app.features.blog_generator.application.result.blog_result import BlogResult
from app.features.blog_generator.application.validator.blog_validator import BlogValidator
from app.features.blog_generator.domain.port.outbound.blog_repository_port import IBlogRepository


class GetBlogService(UseCase[GetBlogQuery, BlogResult]):
    """Retrieve a single blog post by its ID."""

    def __init__(self, blog_repo: IBlogRepository) -> None:
        self._blog_repo = blog_repo

    async def execute(self, input_data: GetBlogQuery) -> BlogResult:
        BlogValidator.validate_get(input_data)

        blog = await self._blog_repo.find_by_id(input_data.blog_id)
        if blog is None:
            raise NotFoundException("BlogContent", input_data.blog_id)

        return BlogMapper.to_result(blog)
