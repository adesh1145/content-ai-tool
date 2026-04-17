from __future__ import annotations

from app.common.exception.base_exception import ValidationException
from app.features.article_writer.application.command.generate_article_command import (
    GenerateArticleCommand,
)


class ArticleValidator:
    @staticmethod
    def validate(command: GenerateArticleCommand) -> None:
        if len(command.topic.strip()) < 10:
            raise ValidationException("Topic must be at least 10 characters long.")
        if not 500 <= command.word_count_target <= 5000:
            raise ValidationException("Word count target must be between 500 and 5000.")
