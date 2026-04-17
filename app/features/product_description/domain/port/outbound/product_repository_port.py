from __future__ import annotations

from abc import abstractmethod

from app.common.port.outbound.repository_port import RepositoryPort
from app.features.product_description.domain.model.product_description import ProductDescription


class ProductRepositoryPort(RepositoryPort[ProductDescription]):
    """Output port for persisting ProductDescription aggregates."""

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> list[ProductDescription]: ...
