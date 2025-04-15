import os
import json
import asyncio

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine

from api.v1 import root_router
from core.config import create_config
from main import create_app, configure_app
from infrastructure.database.postgres.base import Base


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    """
    Создаём общий event_loop для всех асинхронных тестов.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()


@pytest.fixture(scope="session")
def anyio_backend():
    """
    Бэкенд для pytest-anyio (asyncio).
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def redis() -> None:
    """
    Фикстура Redis-клиента (настраивайте под себя).
    """
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", 6379))
    db = int(os.getenv("REDIS_DB", 0))
    redis_client = Redis(host=host, port=port, db=db, decode_responses=True)
    yield redis_client
    await redis_client.aclose()


@pytest.fixture(scope="session", autouse=True)
async def clear_redis(redis: Redis) -> None:
    """
    Очищаем Redis перед/после всех тестов.
    """
    await redis.flushdb()
    yield
    await redis.flushdb()


@pytest.fixture
async def jwt_tokens(redis: Redis):
    """
    Возвращает все токены из Redis по ключу "tokens".
    """
    tokens = await redis.hgetall("tokens")
    return tokens


@pytest.fixture(scope="session", autouse=True)
async def setup_db() -> None:
    """
    Создаём и дропаем тестовую БД.
    """
    DATABASE_TEST_DSN = os.getenv("POSTGRES_DSN", "postgresql+asyncpg://user:pass@localhost:5432/dbtest")
    engine = create_async_engine(DATABASE_TEST_DSN, echo=False, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


@pytest.fixture(scope="module")
async def app() -> FastAPI:
    """
    Создаём FastAPI-приложение иконфигурируем его для e2e-тестов.
    """
    application = create_app()
    config = create_config()
    configure_app(application, root_router, config=config)
    async with LifespanManager(application):
        yield application


@pytest.fixture
async def async_client(app: FastAPI):
    """
    Создаём httpx.AsyncClient для запросов к тестовому приложению.
    """
    async with AsyncClient(
            base_url="http://test",
            transport=ASGITransport(app=app)
    ) as ac:
        yield ac


def pytest_generate_tests(metafunc):
    """
    Автоматически подхватываем маркер @pytest.mark.datafile("<path>").
    Загружаем JSON, раскладываем на (request_data, expected_status).
    """
    marker = metafunc.definition.get_closest_marker("datafile")
    if marker is not None:
        filename = marker.args[0]
        path = os.path.join(metafunc.config.rootdir, filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Вместо трёх (request_data, expected_status, expected_data),
        # теперь у нас только два элемента.
        metafunc.parametrize("request_data, expected_status", data)
