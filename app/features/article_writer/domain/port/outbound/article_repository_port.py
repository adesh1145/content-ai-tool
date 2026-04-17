from __future__ import annotations

from abc import abstractmethod

from app.common.port.outbound.repository_port import RepositoryPort
from app.features.article_writer.domain.model.article import Article


class IArticleRepository(RepositoryPort[Article]):
    @abstractmethod
    async def get_by_user_id(
        self, user_id: str, *, skip: int = 0, limit: int = 50
    ) -> list[Article]: ...
