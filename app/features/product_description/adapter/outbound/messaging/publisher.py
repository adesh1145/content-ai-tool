from __future__ import annotations

import logging

from app.common.domain.domain_event import DomainEvent
from app.common.port.outbound.event_publisher_port import EventPublisherPort

logger = logging.getLogger(__name__)


class ProductEventPublisher(EventPublisherPort):
    """In-memory event publisher for ProductDescription domain events."""

    async def publish(self, event: DomainEvent) -> None:
        logger.info("Product event published: %s [%s]", event.event_type, event.aggregate_id)

    async def publish_all(self, events: list[DomainEvent]) -> None:
        for event in events:
            await self.publish(event)
