from __future__ import annotations

from abc import ABC, abstractmethod

from app.common.domain.domain_event import DomainEvent


class EventPublisherPort(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        ...

    @abstractmethod
    async def publish_all(self, events: list[DomainEvent]) -> None:
        ...
