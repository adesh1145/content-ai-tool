from __future__ import annotations

from app.common.port.inbound.use_case import UseCase
from app.features.auth.application.command.login_command import LoginCommand
from app.features.auth.application.result.token_result import TokenResult


class ILoginUser(UseCase[LoginCommand, TokenResult]):
    """Input port for user login."""
    ...
