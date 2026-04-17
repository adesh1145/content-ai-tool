from __future__ import annotations

from abc import abstractmethod

from app.common.port.outbound.repository_port import RepositoryPort
from app.features.script_writer.domain.model.script import Script


class IScriptRepository(RepositoryPort[Script]):
    """Repository port for the Script aggregate root."""

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> list[Script]: ...
