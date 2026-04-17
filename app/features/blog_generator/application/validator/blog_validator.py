from __future__ import annotations

from app.common.exception.base_exception import ValidationException
from app.features.blog_generator.application.command.generate_blog_command import GenerateBlogCommand
from app.features.blog_generator.application.query.get_blog_query import GetBlogQuery
from app.features.blog_generator.application.query.list_blogs_query import ListBlogsQuery


class BlogValidator:
    """Pre-use-case validation for blog commands and queries."""

    @staticmethod
    def validate_generate(command: GenerateBlogCommand) -> None:
        if not command.user_id:
            raise ValidationException("user_id is required.")
        if not command.topic or len(command.topic.strip()) < 10:
            raise ValidationException("Topic must be at least 10 characters.")
        if command.word_count < 300 or command.word_count > 5000:
            raise ValidationException("Word count must be between 300 and 5000.")

    @staticmethod
    def validate_get(query: GetBlogQuery) -> None:
        if not query.blog_id:
            raise ValidationException("blog_id is required.")

    @staticmethod
    def validate_list(query: ListBlogsQuery) -> None:
        if not query.user_id:
            raise ValidationException("user_id is required.")
        if query.limit < 1 or query.limit > 100:
            raise ValidationException("Limit must be between 1 and 100.")
        if query.offset < 0:
            raise ValidationException("Offset must not be negative.")
