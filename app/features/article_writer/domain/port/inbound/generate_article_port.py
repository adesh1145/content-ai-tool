from __future__ import annotations

from abc import ABC, abstractmethod

from app.features.article_writer.application.command.generate_article_command import (
    GenerateArticleCommand,
)
from app.features.article_writer.application.result.article_result import (
    ArticleResult,
)


class IGenerateArticlePort(ABC):
    @abstractmethod
    async def execute(self, command: GenerateArticleCommand) -> ArticleResult: ...
