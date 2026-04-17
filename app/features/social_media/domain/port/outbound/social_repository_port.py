from __future__ import annotations

from abc import abstractmethod

from app.common.port.outbound.repository_port import RepositoryPort
from app.features.social_media.domain.model.social_post import SocialPost


class ISocialRepository(RepositoryPort[SocialPost]):
    @abstractmethod
    async def get_by_user_id(
        self, user_id: str, *, skip: int = 0, limit: int = 50
    ) -> list[SocialPost]: ...
