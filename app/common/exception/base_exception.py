from __future__ import annotations


class AppException(Exception):
    def __init__(self, message: str, code: str = "APP_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, resource: str, identifier: str = ""):
        detail = f"{resource} not found" + (f": {identifier}" if identifier else "")
        super().__init__(detail, code="NOT_FOUND", status_code=404)


class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, code="CONFLICT", status_code=409)


class ValidationException(AppException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, code="VALIDATION_ERROR", status_code=422)


class AuthenticationException(AppException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, code="UNAUTHORIZED", status_code=401)


class AuthorizationException(AppException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, code="FORBIDDEN", status_code=403)


class RateLimitException(AppException):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, code="RATE_LIMIT", status_code=429)


class LLMProviderException(AppException):
    def __init__(self, provider: str, message: str = "LLM provider error"):
        super().__init__(f"[{provider}] {message}", code="LLM_ERROR", status_code=502)


class QuotaExceededException(AppException):
    def __init__(self, message: str = "Token quota exceeded"):
        super().__init__(message, code="QUOTA_EXCEEDED", status_code=429)
