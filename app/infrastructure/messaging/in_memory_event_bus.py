from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Coroutine
from typing import Any

from app.common.domain.domain_event import DomainEvent
from app.common.port.outbound.event_publisher_port import EventPublisherPort

import logging

logger = logging.getLogger(__name__)

EventHandler = Callable[[DomainEvent], Coroutine[Any, Any, None]]


class InMemoryEventBus(EventPublisherPort):
    """Simple in-memory event bus for domain events."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent) -> None:
        event_type = event.event_type
        handlers = self._handlers.get(event_type, [])
        logger.debug(f"Publishing {event_type} to {len(handlers)} handler(s)")
        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(f"Event handler failed for {event_type}: {e}")

    async def publish_all(self, events: list[DomainEvent]) -> None:
        for event in events:
            await self.publish(event)


_event_bus: InMemoryEventBus | None = None


def get_event_bus() -> InMemoryEventBus:
    global _event_bus
    if _event_bus is None:
        _event_bus = InMemoryEventBus()
    return _event_bus
