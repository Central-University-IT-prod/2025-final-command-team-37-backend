from typing import Iterable

from dishka import Provider

from .providers import (
    ConfigProvider,
    PostgresProvider,
    RedisProvider,
    InteractorProvider,
    AuthProvider,
    RepositoryProvider,
)


def get_providers() -> Iterable[Provider]:
    return (
        ConfigProvider(),
        PostgresProvider(),
        RedisProvider(),
        InteractorProvider(),
        AuthProvider(),
        RepositoryProvider(),
    )
