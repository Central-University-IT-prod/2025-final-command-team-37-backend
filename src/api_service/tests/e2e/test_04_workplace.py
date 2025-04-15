import pytest


@pytest.mark.datafile("tests/e2e/components/workplace/upsert_workplace_data.json")
@pytest.mark.anyio
async def test_upsert_workplace(async_client, request_data, expected_status, jwt_tokens, redis):
    """
    Проверяет создание/обновление рабочего места через эндпоинт /v1/workplace/upsert.
    Перед этим создается тариф через /v1/coworking/tariffs/add, идентификатор которого используется в тестовых данных.
    Сохранённый идентификатор рабочего места сохраняется в Redis.
    """
    token = jwt_tokens.get("jwt")
    coworking_id = await redis.hget("tokens", "coworking_id")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    # Создаем тариф, который понадобится для рабочего места
    tariff_payload = [
        {
            "coworking_id": coworking_id,
            "name": "VIP",
            "color": "#4CA50F",
            "price_per_hour": 750
        }
    ]
    tariff_response = await async_client.post("/v1/coworking/tariffs/add", json=tariff_payload, headers=headers)
    assert tariff_response.status_code == 201
    tariff_data = tariff_response.json()
    tariff_id = tariff_data[0].get("id")
    assert tariff_id is not None

    # Устанавливаем тариф и coworking_id для каждого рабочего места
    for item in request_data:
        item["coworking_id"] = coworking_id
        item["tariff_id"] = tariff_id

    response = await async_client.post("/v1/workplace/upsert", json=request_data, headers=headers)
    assert response.status_code == expected_status
    data = response.json()
    assert isinstance(data, list)
    if data:
        workplace_id = data[0].get("id")
        assert workplace_id is not None
        await redis.hset("tokens", "workplace_id", workplace_id)
