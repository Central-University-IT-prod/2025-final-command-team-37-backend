from enum import StrEnum
from datetime import datetime
from typing import Annotated, List

from pydantic import Field, constr, conint, confloat, UUID4


class UserRole(StrEnum):
    USER = 'USER'
    ADMIN = 'ADMIN'


class WorkplaceStatus(StrEnum):
    FREE = 'FREE'
    BOOKED = 'BOOKED'
    INACTIVE = 'INACTIVE'


class BookingStatus(StrEnum):
    WAITING = 'WAITING'
    PROCESSING = 'PROCESSING'
    FINISHED = 'FINISHED'


TgId = Annotated[
    conint(ge=1),
    Field(ge=1, examples=[1522105862])
]
FirstName = Annotated[
    constr(min_length=1),
    Field(min_length=1, examples=['Дмитрий'])
]
LastName = Annotated[
    constr(min_length=0),
    Field(min_length=0, examples=['Нагиев'])
]
Username = Annotated[
    constr(min_length=1),
    Field(min_length=1, examples=['parapopovich'])
]
AuthDate = Annotated[
    conint(ge=0),
    Field(ge=0, examples=[1742720967])
]
TgHash = Annotated[
    constr(min_length=1),
    Field(min_length=1, examples=['035da2b6954c0e8dfd8de9a10b6644152a66c03aadda72205fec89806e0fc9b3'])
]
PhotoUrl = Annotated[
    constr(min_length=0),
    Field(min_length=0, examples=['https://t.me/i/userpic/320/7IQwLdFc8nusS8VT2ll1tQnEW8pKzd3wP-s_SbiBsmY.svg'])
]
UserBalance = Annotated[
    conint(ge=0),
    Field(ge=0, examples=[4252])
]

CoworkingId = Annotated[
    UUID4,
    Field(examples=['487dec82-396e-4cf3-b555-86cc5db6b415'])
]
CoworkingName = Annotated[
    constr(min_length=1),
    Field(min_length=1, examples=['Коворкинг на Ленина'])
]
CoworkingAddress = Annotated[
    constr(min_length=1),
    Field(min_length=1, examples=['г. Москва, ул. Ленина, 10'])
]
CoworkingDescription = Annotated[
    constr(min_length=0),
    Field(min_length=0, examples=['Коворкинг на Ленина - это пространство для работы и общения'])
]
CoworkingPhotoUrl = Annotated[
    constr(min_length=1),
    Field(min_length=1, examples=[
        'https://prod-team-37-ajc3mefd.REDACTED/api/v1/cdn/file/99216f07-ecb3-4b70-9fd6-1bbdae5d3104.jpeg'])
]
CoworkingCoverUrl = Annotated[
    constr(min_length=1),
    Field(min_length=1, examples=[
        'https://prod-team-37-ajc3mefd.REDACTED/api/v1/cdn/file/a078d506-a6e9-4f50-9a01-604c85ac4049.jpeg'])
]

TariffId = Annotated[
    UUID4,
    Field(examples=['fe8279bc-2d9c-43ea-985c-0f3f53981335'])
]
TariffName = Annotated[
    constr(min_length=1),
    Field(min_length=1, examples=['VIP'])
]
TariffColor = Annotated[
    constr(min_length=1),
    Field(min_length=1, examples=['#4CA50F'])
]
TariffPricePerHour = Annotated[
    conint(ge=0),
    Field(ge=0, examples=[750])
]

WorkplaceId = Annotated[
    UUID4,
    Field(examples=['57f25aa0-ea44-4aa6-892f-1c3ebf1cab1b'])
]
WorkplaceNumber = Annotated[
    conint(ge=1),
    Field(ge=1, examples=[14])
]
WorkplaceName = Annotated[
    constr(min_length=1),
    Field(min_length=1, examples=['Стол 14'])
]
WorkplaceXCor = Annotated[
    confloat(ge=0),
    Field(examples=[37.21])
]
WorkplaceYCor = Annotated[
    confloat(ge=0),
    Field(examples=[55.75])
]
WorkplaceTags = Annotated[
    List[str],
    Field(examples=[['Комфортный стол', 'Кресло', 'Кофемашина']])
]

BookingId = Annotated[
    UUID4,
    Field(examples=['f3047cd8-56e6-46e4-ac2d-757550c1f62a'])
]
BookingStartTime = Annotated[
    datetime,
    Field(ge=0, examples=[datetime.now()])
]
BookingEndTime = Annotated[
    datetime,
    Field(ge=0, examples=[datetime.now()])
]
BookingTotalPrice = Annotated[
    conint(ge=0),
    Field(ge=0, examples=[1500])
]

CreatedAt = Annotated[
    datetime,
    Field(ge=0, examples=[datetime.now()])
]
