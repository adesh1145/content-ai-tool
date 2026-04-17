from __future__ import annotations

from app.common.domain.domain_event import DomainEvent
from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.infrastructure.messaging.in_memory_event_bus import get_event_bus


class AuthEventPublisher(EventPublisherPort):
    """Driven adapter — delegates to the shared InMemoryEventBus singleton."""

    def __init__(self) -> None:
        self._bus = get_event_bus()

    async def publish(self, event: DomainEvent) -> None:
        await self._bus.publish(event)

    async def publish_all(self, events: list[DomainEvent]) -> None:
        await self._bus.publish_all(events)
