from __future__ import annotations

from app.common.exception.base_exception import NotFoundException


class UserNotFoundError(NotFoundException):
    """Raised when a user cannot be found."""

    def __init__(self, identifier: str) -> None:
        super().__init__(resource="User", identifier=identifier)
