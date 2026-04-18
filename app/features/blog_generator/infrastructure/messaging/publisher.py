from __future__ import annotations

from app.common.domain.domain_event import DomainEvent
from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.infrastructure.messaging.in_memory_event_bus import get_event_bus


class BlogEventPublisher(EventPublisherPort):
    """Delegates to the shared in-memory event bus."""

    async def publish(self, event: DomainEvent) -> None:
        bus = get_event_bus()
        await bus.publish(event)

    async def publish_all(self, events: list[DomainEvent]) -> None:
        bus = get_event_bus()
        await bus.publish_all(events)
