from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine
from redis.asyncio import Redis

from core.config import (
    PostgresConfig,
    RedisConfig,
)
from core.utils import is_valid_postgres_uri
from infrastructure.database.postgres.session import create_engine
from infrastructure.database.redis.session import get_redis


class PostgresProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_db_engine(self, config: PostgresConfig) -> AsyncIterable[AsyncEngine]:
        DB_URI = config.POSTGRES_DSN.replace("postgresql://", "postgresql+asyncpg://")
        if not is_valid_postgres_uri(config.POSTGRES_DSN):
            host = config.POSTGRES_HOST
            port = config.POSTGRES_PORT
            username = config.POSTGRES_USERNAME
            password = config.POSTGRES_PASSWORD
            db_name = config.POSTGRES_DATABASE

            DB_URI = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}"

        async for engine in create_engine(DB_URI=DB_URI):
            yield engine


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_redis_client(self, config: RedisConfig) -> AsyncIterable[Redis]:
        async for redis in get_redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                db=config.REDIS_DB,
        ):
            yield redis
