import datetime
import pytest
from domain.dto.user import UserDTO, TelegramAuthDTO
from domain.dto.misc import UserRole


# Вспомогательный класс для эмуляции ORM-объекта
class DummyORM:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_user_dto_orm_conversion():
    """
    Проверяет преобразование ORM-представления в UserDTO.
    Здесь ORM-представление смоделировано с помощью DummyORM.
    """
    dummy_orm = DummyORM(
        id=1522105862,
        first_name="Дмитрий",
        last_name="Нагиев",
        username="parapopovich",
        photo_url="https://example.com/photo.jpg",
        balance=11000,
        role="USER",
        created_at=datetime.datetime(2025, 3, 4, 9, 0, 0)
    )
    dto = UserDTO.orm_to_dto(dummy_orm)
    assert str(dto.id) == str(dummy_orm.id)
    assert dto.first_name == dummy_orm.first_name
    assert dto.balance == dummy_orm.balance


def test_telegram_auth_dto_to_orm():
    """
    Проверяет преобразование из TelegramAuthDTO в ORM-объект.
    Метод dto_to_orm должен вернуть объект с соответствующими атрибутами.
    """
    auth = TelegramAuthDTO(
        id=1522105862,
        first_name="Дмитрий",
        last_name="Нагиев",
        username="parapopovich",
        photo_url="https://example.com/photo.jpg",
        auth_date=1742720967,
        hash="somehash"
    )
    user_orm = auth.dto_to_orm(UserRole.USER)
    assert user_orm.id == auth.id
    assert user_orm.first_name == auth.first_name
