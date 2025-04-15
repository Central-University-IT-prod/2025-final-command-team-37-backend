import datetime
import pytest
from domain.dto.coworking import CoworkingDTO, CoworkingTariffDTO


class DummyORM:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_coworking_dto_orm_conversion():
    """
    Проверяет преобразование ORM-представления в CoworkingDTO.
    """
    dummy_orm = DummyORM(
        id="487dec82-396e-4cf3-b555-86cc5db6b415",
        name="Коворкинг на Ленина",
        address="г. Москва, ул. Ленина, 10",
        photo_url="https://example.com/photo.jpg",
        cover_url="https://example.com/cover.jpg",
        description="Пространство для работы",
        created_at=datetime.datetime(2025, 3, 4, 9, 0, 0)
    )
    dto = CoworkingDTO.orm_to_dto(dummy_orm)
    assert str(dto.id) == dummy_orm.id
    assert dto.name == dummy_orm.name


def test_coworking_tariff_dto_orm_conversion():
    """
    Проверяет преобразование ORM-представления в CoworkingTariffDTO.
    """
    dummy_orm = DummyORM(
        id="fe8279bc-2d9c-43ea-985c-0f3f53981335",
        name="VIP",
        color="#4CA50F",
        price_per_hour=750,
        created_at=datetime.datetime(2025, 3, 4, 9, 0, 0)
    )
    dto = CoworkingTariffDTO.orm_to_dto(dummy_orm)
    assert str(dto.id) == dummy_orm.id
    assert dto.name == dummy_orm.name
    assert dto.price_per_hour == dummy_orm.price_per_hour
