import datetime
import pytest
from domain.dto.workplace import WorkplaceDTO, WorkplaceUpsertDTO


class DummyORM:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_workplace_dto_orm_conversion():
    """
    Проверяет преобразование ORM-представления в WorkplaceDTO,
    включая вложенный объект тарифа.
    """
    dummy_tariff = DummyORM(
        id="fe8279bc-2d9c-43ea-985c-0f3f53981335",
        name="VIP",
        color="#4CA50F",
        price_per_hour=750,
        created_at=datetime.datetime(2025, 3, 4, 9, 0, 0)
    )
    dummy_orm = DummyORM(
        id="57f25aa0-ea44-4aa6-892f-1c3ebf1cab1b",
        number=14,
        name="Стол 14",
        status="FREE",
        x_cor=37.21,
        y_cor=55.75,
        tariff=dummy_tariff,
        created_at=datetime.datetime(2025, 3, 4, 9, 0, 0)
    )
    dto = WorkplaceDTO.orm_to_dto(dummy_orm)
    assert str(dto.id) == dummy_orm.id
    assert dto.name == dummy_orm.name
    assert dto.tariff.name == dummy_tariff.name


def test_workplace_upsert_dto_dict():
    """
    Проверяет, что метод dict() в WorkplaceUpsertDTO возвращает корректный словарь.
    При сравнении преобразуем поля UUID в строки.
    """
    dto = WorkplaceUpsertDTO(
        coworking_id="487dec82-396e-4cf3-b555-86cc5db6b415",
        tariff_id="fe8279bc-2d9c-43ea-985c-0f3f53981335",
        number=14,
        name="Стол 14",
        tags=["Комфортный стол", "Кресло", "Кофемашина"],
        x_cor=37.21,
        y_cor=55.75
    )
    result = dto.dict()
    expected = {
        "coworking_id": "487dec82-396e-4cf3-b555-86cc5db6b415",
        "tariff_id": "fe8279bc-2d9c-43ea-985c-0f3f53981335",
        "number": 14,
        "name": "Стол 14",
        "tags": ["Комфортный стол", "Кресло", "Кофемашина"],
        "x_cor": 37.21,
        "y_cor": 55.75
    }
    for key in ("coworking_id", "tariff_id"):
        result[key] = str(result[key])
    assert result == expected
