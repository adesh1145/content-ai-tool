from __future__ import annotations

from app.common.port.inbound.use_case import UseCase
from app.features.auth.application.result.token_result import AccessTokenResult


class IRefreshToken(UseCase[str, AccessTokenResult]):
    """Input port for refreshing an access token."""
    ...
