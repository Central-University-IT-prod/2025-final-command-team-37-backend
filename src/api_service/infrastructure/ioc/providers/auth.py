from dishka import Provider, Scope, provide

from core.security import AuthManager
from core.config import SecurityConfig


class AuthProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_auth_service(self, config: SecurityConfig) -> AuthManager:
        return AuthManager(config)
