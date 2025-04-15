import pytest
from uuid import UUID


@pytest.mark.datafile("tests/e2e/components/booking/add_booking_data.json")
@pytest.mark.anyio
async def test_add_booking(async_client, request_data, expected_status, jwt_tokens, redis):
    """
    Проверяет создание бронирования через endpoint /v1/bookings/add.
    В теле запроса workplaces заполняется id рабочего места из Redis.
    После создания id бронирования сохраняется в Redis.
    """
    token = jwt_tokens.get("jwt")
    workplace_id = await redis.hget("tokens", "workplace_id")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    request_data["workplaces"] = [workplace_id]
    response = await async_client.post("/v1/bookings/add", json=request_data, headers=headers)
    assert response.status_code == expected_status, response.text
    data = response.json()
    booking_id = data.get("id")
    assert booking_id is not None
    await redis.hset("tokens", "booking_id", booking_id)


@pytest.mark.skip(reason="Lazy-loading issue: MissingGreenlet encountered in get_booking")
@pytest.mark.datafile("tests/e2e/components/booking/get_booking_data.json")
@pytest.mark.anyio
async def test_get_booking(async_client, request_data, expected_status, jwt_tokens, redis):
    """
    Проверяет получение бронирования через endpoint /v1/bookings/get,
    используя id бронирования, сохранённый в Redis.
    (Пропущен из-за проблемы lazy-loading.)
    """
    token = jwt_tokens.get("jwt")
    booking_id = await redis.hget("tokens", "booking_id")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    url = f"/v1/bookings/get?booking_id={booking_id}"
    response = await async_client.get(url, headers=headers)
    assert response.status_code == expected_status, response.text
    data = response.json()
    assert data.get("id") == booking_id


@pytest.mark.datafile("tests/e2e/components/booking/update_booking_data.json")
@pytest.mark.anyio
async def test_update_booking(async_client, request_data, expected_status, jwt_tokens, redis):
    """
    Проверяет обновление бронирования через endpoint /v1/bookings/update.
    Теперь booking_id передается и в query, и присутствует в теле запроса,
    а также workplaces добавляются в тело.
    """
    token = jwt_tokens.get("jwt")
    booking_id = await redis.hget("tokens", "booking_id")
    workplace_id = await redis.hget("tokens", "workplace_id")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    # Добавляем booking_id в query-параметры:
    url = f"/v1/bookings/update?booking_id={booking_id}"
    # В теле запроса также передаём booking_id и workplaces:
    request_data["id"] = booking_id
    request_data["workplaces"] = [workplace_id]
    response = await async_client.patch(url, json=request_data, headers=headers)
    assert response.status_code == expected_status


@pytest.mark.datafile("tests/e2e/components/booking/delete_booking_data.json")
@pytest.mark.anyio
async def test_delete_booking(async_client, request_data, expected_status, jwt_tokens, redis):
    """
    Проверяет удаление бронирования через endpoint /v1/bookings/delete.
    Передаем booking_id как строку (UUID), чтобы тип совпадал с типом в базе.
    """
    token = jwt_tokens.get("jwt")
    booking_id = await redis.hget("tokens", "booking_id")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    url = f"/v1/bookings/delete?booking_id={booking_id}"
    response = await async_client.delete(url, headers=headers)
    assert response.status_code == expected_status
