import datetime
import pytest
from domain.dto.base import BaseDTO


def test_base_dto_dict_excludes_none():
    """
    Проверяет, что метод dict() базового DTO исключает значения None.
    """

    class DummyDTO(BaseDTO):
        a: int = 1
        b: str = None

    instance = DummyDTO()
    result = instance.dict()
    assert result == {"a": 1}


def test_validate_fields_success():
    """
    Проверяет, что валидатор в BaseDTO не генерирует ошибку,
    если start_time меньше end_time.
    """

    class DummyBookingDTO(BaseDTO):
        start_time: datetime.datetime
        end_time: datetime.datetime

    now = datetime.datetime.now()
    later = now + datetime.timedelta(hours=1)
    instance = DummyBookingDTO(start_time=now, end_time=later)
    assert instance.start_time < instance.end_time


def test_validate_fields_failure():
    """
    Проверяет, что валидатор в BaseDTO генерирует ошибку,
    если start_time больше end_time.
    """

    class DummyBookingDTO(BaseDTO):
        start_time: datetime.datetime
        end_time: datetime.datetime

    now = datetime.datetime.now()
    earlier = now - datetime.timedelta(hours=1)
    with pytest.raises(ValueError, match="start_time must be less than end_time"):
        DummyBookingDTO(start_time=now, end_time=earlier)
