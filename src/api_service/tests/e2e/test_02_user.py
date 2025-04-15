import pytest


@pytest.mark.datafile("tests/e2e/components/user/auth_valid_data.json")
@pytest.mark.anyio
async def test_auth_user(async_client, request_data, expected_status, redis):
    """
    Выполняет авторизацию пользователя через эндпоинт /v1/user/auth.
    При успешном ответе JWT-токен сохраняется в Redis.
    """
    response = await async_client.post("/v1/user/auth", json=request_data)
    assert response.status_code == expected_status
    token = response.json().get("token")
    assert token is not None
    await redis.hset("tokens", "jwt", token)


@pytest.mark.datafile("tests/e2e/components/user/get_profile_data.json")
@pytest.mark.anyio
async def test_get_profile(async_client, request_data, expected_status, jwt_tokens):
    """
    Проверяет получение профиля пользователя через эндпоинт /v1/user/profile,
    используя сохранённый JWT-токен.
    """
    token = jwt_tokens.get("jwt")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = await async_client.get("/v1/user/profile", headers=headers)
    assert response.status_code == expected_status


@pytest.mark.datafile("tests/e2e/components/user/list_users_data.json")
@pytest.mark.anyio
async def test_list_users(async_client, request_data, expected_status, jwt_tokens):
    """
    Проверяет получение списка пользователей через эндпоинт /v1/user/list,
    используя сохранённый JWT-токен.
    """
    token = jwt_tokens.get("jwt")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = await async_client.get("/v1/user/list", headers=headers)
    assert response.status_code == expected_status
    data = response.json()
    assert isinstance(data, list)
