import datetime
import pytest
from domain.dto.booking import BookingDTO, BookingCreateDTO, BookingUpdateDTO
from domain.dto.workplace import WorkplaceDTO
from uuid import UUID


class DummyORM:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_booking_dto_orm_conversion():
    """
    Проверяет преобразование ORM-представления в BookingDTO,
    включая вложенные объекты рабочего места.
    """
    dummy_workplace = DummyORM(
        id="57f25aa0-ea44-4aa6-892f-1c3ebf1cab1b",
        number=14,
        name="Стол 14",
        status="FREE",
        x_cor=37.21,
        y_cor=55.75,
        tariff=DummyORM(
            id="fe8279bc-2d9c-43ea-985c-0f3f53981335",
            name="VIP",
            color="#4CA50F",
            price_per_hour=750,
            created_at=datetime.datetime(2025, 3, 4, 9, 0, 0)
        ),
        created_at=datetime.datetime(2025, 3, 4, 9, 0, 0)
    )
    dummy_orm = DummyORM(
        id="f3047cd8-56e6-46e4-ac2d-757550c1f62a",
        user_id=1522105862,
        workplaces=[dummy_workplace],
        start_time=datetime.datetime(2025, 3, 4, 9, 0, 0),
        end_time=datetime.datetime(2025, 3, 4, 10, 0, 0),
        status="WAITING",
        total_price=1500,
        created_at=datetime.datetime(2025, 3, 4, 9, 0, 0)
    )
    dto = BookingDTO.orm_to_dto(dummy_orm)
    assert str(dto.id) == dummy_orm.id
    assert dto.total_price == dummy_orm.total_price
    assert dto.workplaces[0].name == dummy_workplace.name


def test_booking_create_dto_validation():
    """
    Проверяет валидацию BookingCreateDTO:
    корректные данные проходят, а если start_time больше end_time – генерируется ошибка.
    """
    now = datetime.datetime(2025, 3, 4, 9, 0, 0)
    later = datetime.datetime(2025, 3, 4, 10, 0, 0)
    dto = BookingCreateDTO(
        workplaces=["57f25aa0-ea44-4aa6-892f-1c3ebf1cab1b"],
        start_time=now,
        end_time=later,
    )
    assert dto.start_time < dto.end_time
    with pytest.raises(ValueError, match="start_time must be less than end_time"):
        BookingCreateDTO(
            workplaces=["57f25aa0-ea44-4aa6-892f-1c3ebf1cab1b"],
            start_time=later,
            end_time=now,
        )


def test_booking_update_dto():
    """
    Проверяет, что BookingUpdateDTO корректно создается с опциональными полями.
    """
    dto = BookingUpdateDTO(start_time=None, end_time=None)
    assert dto.start_time is None and dto.end_time is None
