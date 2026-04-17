from __future__ import annotations

from dataclasses import dataclass, field

from app.common.domain.base_entity import BaseEntity
from app.common.domain.domain_event import DomainEvent


@dataclass
class AggregateRoot(BaseEntity):
    _domain_events: list[DomainEvent] = field(default_factory=list, repr=False)

    def register_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events

    @property
    def domain_events(self) -> list[DomainEvent]:
        return list(self._domain_events)
