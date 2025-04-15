import pytest


@pytest.mark.datafile("tests/e2e/components/coworking/add_coworking_data.json")
@pytest.mark.anyio
async def test_add_coworking(async_client, request_data, expected_status, jwt_tokens, redis):
    """
    Проверяет создание коворкинга через эндпоинт /v1/coworking/add.
    Сохранённый идентификатор коворкинга помещается в Redis.
    """
    token = jwt_tokens.get("jwt")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = await async_client.post("/v1/coworking/add", json=request_data, headers=headers)
    assert response.status_code == expected_status
    data = response.json()
    coworking_id = data.get("id")
    assert coworking_id is not None
    await redis.hset("tokens", "coworking_id", coworking_id)


@pytest.mark.datafile("tests/e2e/components/coworking/get_coworking_data.json")
@pytest.mark.anyio
async def test_get_coworking(async_client, request_data, expected_status, jwt_tokens, redis):
    """
    Проверяет получение данных коворкинга через эндпоинт /v1/coworking/{coworking_id}/get,
    используя идентификатор из Redis.
    """
    token = jwt_tokens.get("jwt")
    coworking_id = await redis.hget("tokens", "coworking_id")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    url = f"/v1/coworking/{coworking_id}/get"
    response = await async_client.get(url, headers=headers)
    assert response.status_code == expected_status
    data = response.json()
    for key, value in request_data.items():
        assert data.get(key) == value


@pytest.mark.datafile("tests/e2e/components/coworking/list_coworking_data.json")
@pytest.mark.anyio
async def test_list_coworkings(async_client, request_data, expected_status, jwt_tokens):
    """
    Проверяет получение списка коворкингов через эндпоинт /v1/coworking/list.
    """
    token = jwt_tokens.get("jwt")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = await async_client.get("/v1/coworking/list", headers=headers)
    assert response.status_code == expected_status
    data = response.json()
    assert isinstance(data, list)
