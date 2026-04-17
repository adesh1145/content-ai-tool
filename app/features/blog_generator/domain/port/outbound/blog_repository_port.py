from __future__ import annotations

from abc import abstractmethod

from app.common.port.outbound.repository_port import RepositoryPort
from app.features.blog_generator.domain.model.blog_content import BlogContent


class IBlogRepository(RepositoryPort[BlogContent]):
    """Output port for blog persistence."""

    @abstractmethod
    async def list_by_user(
        self, user_id: str, *, limit: int = 20, offset: int = 0
    ) -> list[BlogContent]: ...
