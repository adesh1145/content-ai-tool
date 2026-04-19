from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.auth.domain.port.outbound.user_repository_port import IUserRepository
from app.features.auth.domain.port.outbound.token_service_port import ITokenService
from app.features.auth.application.port.inbound.register_user_port import IRegisterUser
from app.features.auth.application.port.inbound.login_user_port import ILoginUser
from app.features.auth.application.port.inbound.refresh_token_port import IRefreshToken

from app.features.auth.infrastructure.messaging.publisher import AuthEventPublisher
from app.features.auth.infrastructure.persistence.repository import SQLAlchemyUserRepository
from app.features.auth.infrastructure.security.jwt_token_service import JWTTokenService
from app.features.auth.application.service.login_user_service import LoginUserService
from app.features.auth.application.service.refresh_token_service import RefreshTokenService
from app.features.auth.application.service.register_user_service import RegisterUserService


class AuthContainer:
    """Per-request DI container for the Auth bounded context.

    Usage in routes::

        container = AuthContainer(db_session)
        result = await container.register_use_case.execute(command)
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._user_repo = SQLAlchemyUserRepository(session)
        self._token_service = JWTTokenService()
        self._event_publisher = AuthEventPublisher()

    @property
    def user_repo(self) -> IUserRepository:
        return self._user_repo

    @property
    def event_publisher(self) -> EventPublisherPort:
        return self._event_publisher

    @property
    def token_service(self) -> ITokenService:
        return self._token_service

    @property
    def register_use_case(self) -> IRegisterUser:
        return RegisterUserService(
            user_repo=self._user_repo,
            event_publisher=self._event_publisher,
        )

    @property
    def login_use_case(self) -> ILoginUser:
        return LoginUserService(
            user_repo=self._user_repo,
            token_service=self._token_service,
            event_publisher=self._event_publisher,
        )

    @property
    def refresh_use_case(self) -> IRefreshToken:
        return RefreshTokenService(
            user_repo=self._user_repo,
            token_service=self._token_service,
        )
