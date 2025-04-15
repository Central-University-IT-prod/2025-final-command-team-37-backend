import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_ping(async_client: AsyncClient):
    """
    Тест для эндпоинта /v1/ping

    Полезные данные: request_data
    Отклик: {"ping": "pong-pong-pong"}
    Проверяем, что эндпоинт доступен и возвращает корректный статус 200
    """
    response = await async_client.get("/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong-pong-pong"}
