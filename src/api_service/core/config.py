from typing import Optional, List
from dataclasses import dataclass

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")


class ServerConfig(BaseConfig):
    SERVER_HOST: Optional[str] = "0.0.0.0"
    SERVER_PORT: Optional[int] = 8080


class PostgresConfig(BaseConfig):
    POSTGRES_DSN: Optional[str]
    POSTGRES_USERNAME: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_HOST: Optional[str]
    POSTGRES_PORT: Optional[int]
    POSTGRES_DATABASE: Optional[str]


class RedisConfig(BaseConfig):
    REDIS_HOST: Optional[str] = "127.0.0.1"
    REDIS_PORT: Optional[int] = 6379
    REDIS_DB: Optional[int] = 0

class CDNConfig(BaseConfig):
    STORAGE_PATH: str


class SecurityConfig(BaseConfig):
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = 60
    SECRET_KEY: str
    ALGORITHM: str

    TG_ADMINS: List[int]


@dataclass(frozen=True)
class Config:
    server: ServerConfig
    postgres: PostgresConfig
    redis: RedisConfig
    cdn: CDNConfig
    security: SecurityConfig


def create_config() -> Config:
    return Config(
        server=ServerConfig(),
        postgres=PostgresConfig(),
        redis=RedisConfig(),
        cdn=CDNConfig(),
        security=SecurityConfig()
    )
