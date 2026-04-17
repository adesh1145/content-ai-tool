from __future__ import annotations

from app.common.port.inbound.use_case import UseCase
from app.features.blog_generator.application.command.generate_blog_command import GenerateBlogCommand
from app.features.blog_generator.application.result.blog_result import BlogResult


class IGenerateBlog(UseCase[GenerateBlogCommand, BlogResult]):
    """Input port for the blog generation use case."""
    ...
