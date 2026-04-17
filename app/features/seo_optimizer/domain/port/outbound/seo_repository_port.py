from __future__ import annotations

from abc import abstractmethod

from app.common.port.outbound.repository_port import RepositoryPort
from app.features.seo_optimizer.domain.model.seo_analysis import SEOAnalysis


class ISEORepository(RepositoryPort[SEOAnalysis]):
    """Repository port for the SEOAnalysis aggregate root."""

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> list[SEOAnalysis]: ...
