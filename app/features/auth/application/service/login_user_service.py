from __future__ import annotations

from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.auth.application.command.login_command import LoginCommand
from app.features.auth.application.result.token_result import TokenResult
from app.features.auth.domain.event.user_logged_in_event import UserLoggedInEvent
from app.features.auth.domain.exception.invalid_credentials import InvalidCredentialsError
from app.features.auth.application.port.inbound.login_user_port import ILoginUser
from app.features.auth.domain.port.outbound.token_service_port import ITokenService
from app.features.auth.domain.port.outbound.user_repository_port import IUserRepository
from app.features.auth.domain.service.password_service import PasswordService


class LoginUserService(ILoginUser):
    """Authenticate credentials, issue JWT token pair, publish login event."""

    def __init__(
        self,
        user_repo: IUserRepository,
        token_service: ITokenService,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._user_repo = user_repo
        self._token_service = token_service
        self._event_publisher = event_publisher

    async def execute(self, input_data: LoginCommand) -> TokenResult:
        user = await self._user_repo.get_by_email(input_data.email.lower())

        if not user or not PasswordService.verify(
            input_data.password, user.hashed_password
        ):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InvalidCredentialsError("Account is deactivated.")

        access_token = self._token_service.create_access_token(
            user_id=user.id, email=str(user.email)
        )
        refresh_token = self._token_service.create_refresh_token(user_id=user.id)

        await self._event_publisher.publish(
            UserLoggedInEvent(
                aggregate_id=user.id,
                email=str(user.email),
            )
        )

        return TokenResult(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self._token_service.get_access_token_expire_seconds(),
        )
