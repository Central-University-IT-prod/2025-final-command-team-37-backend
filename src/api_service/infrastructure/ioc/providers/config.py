from dishka import Provider, Scope, provide, from_context

from core.config import (
    Config,
    create_config,
    ServerConfig,
    PostgresConfig,
    RedisConfig,
    CDNConfig,
    SecurityConfig,
)


class ConfigProvider(Provider):
    scope = Scope.APP
    config = from_context(provides=Config)

    @provide
    def get_config(self) -> Config:
        return create_config()

    @provide
    def get_server_config(self, config: Config) -> ServerConfig:
        return config.server

    @provide
    def get_postgres_config(self, config: Config) -> PostgresConfig:
        return config.postgres

    @provide
    def get_redis_config(self, config: Config) -> RedisConfig:
        return config.redis

    @provide
    def get_cdn_config(self, config: Config) -> CDNConfig:
        return config.cdn

    @provide
    def get_security_config(self, config: Config) -> SecurityConfig:
        return config.security
