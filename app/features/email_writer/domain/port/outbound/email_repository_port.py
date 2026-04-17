from __future__ import annotations

from abc import abstractmethod

from app.common.port.outbound.repository_port import RepositoryPort
from app.features.email_writer.domain.model.email_content import EmailContent


class EmailRepositoryPort(RepositoryPort[EmailContent]):
    """Output port for persisting EmailContent aggregates."""

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> list[EmailContent]: ...
