from __future__ import annotations


class HashedPassword:
    """Immutable value object wrapping a bcrypt-hashed password string."""

    __slots__ = ("_hash",)

    def __init__(self, hashed: str) -> None:
        self._hash = hashed

    @property
    def value(self) -> str:
        return self._hash

    def __str__(self) -> str:
        return self._hash

    def __repr__(self) -> str:
        return "HashedPassword(***)"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HashedPassword):
            return self._hash == other._hash
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._hash)
