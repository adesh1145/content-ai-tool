"""
app/core/interfaces/base_repository.py
─────────────────────────────────────────────────────────────
Generic abstract repository interface (ISP + DIP).

SOLID:
  - ISP: Features define their own specific sub-interfaces.
  - DIP: Use cases depend on this abstraction, never on SQLAlchemy.

Clean Architecture Layer 2: Use Cases depend on this interface,
not on any concrete DB implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.core.entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class IRepository(ABC, Generic[T]):
    """
    Generic CRUD repository contract.

    Concrete implementations live in each feature's
    `adapters/` layer (e.g. BlogGateway, UserGateway).
    """

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Persist (insert or update) an entity. Returns the saved entity."""
        ...

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> T | None:
        """Fetch a single entity by its UUID. Returns None if not found."""
        ...

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Soft or hard delete. Returns True if deleted, False if not found."""
        ...
