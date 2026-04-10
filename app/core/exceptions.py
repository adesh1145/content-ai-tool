"""
app/core/exceptions.py
─────────────────────────────────────────────────────────────
Domain exceptions hierarchy.

All custom exceptions inherit from DomainException.
FastAPI exception handlers map these to HTTP responses
in app/main.py — keeping HTTP concerns out of use cases.
"""

from __future__ import annotations


class DomainException(Exception):
    """Root of all domain exceptions."""
    def __init__(self, message: str, code: str = "DOMAIN_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class NotFoundError(DomainException):
    """Entity not found in the repository."""
    def __init__(self, entity: str, entity_id: str) -> None:
        super().__init__(
            message=f"{entity} with id '{entity_id}' not found.",
            code="NOT_FOUND",
        )


class ValidationError(DomainException):
    """Domain-level validation failure."""
    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="VALIDATION_ERROR")


class AuthenticationError(DomainException):
    """Invalid credentials or expired token."""
    def __init__(self, message: str = "Authentication failed.") -> None:
        super().__init__(message=message, code="AUTHENTICATION_ERROR")


class AuthorizationError(DomainException):
    """Authenticated user lacks permission."""
    def __init__(self, message: str = "Permission denied.") -> None:
        super().__init__(message=message, code="AUTHORIZATION_ERROR")


class QuotaExceededError(DomainException):
    """User has exceeded their monthly usage quota."""
    def __init__(self, used: int, limit: int) -> None:
        super().__init__(
            message=f"Monthly quota exceeded. Used: {used}, Limit: {limit}.",
            code="QUOTA_EXCEEDED",
        )


class LLMProviderError(DomainException):
    """LLM API call failed (rate limit, timeout, etc.)."""
    def __init__(self, provider: str, detail: str) -> None:
        super().__init__(
            message=f"LLM provider '{provider}' error: {detail}",
            code="LLM_PROVIDER_ERROR",
        )


class DuplicateError(DomainException):
    """Attempt to create a duplicate entity."""
    def __init__(self, entity: str, field: str, value: str) -> None:
        super().__init__(
            message=f"{entity} with {field}='{value}' already exists.",
            code="DUPLICATE_ERROR",
        )
