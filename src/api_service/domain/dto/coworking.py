from typing import Optional

from .base import BaseDTO
from .misc import (
    CoworkingId,
    CoworkingName,
    CoworkingAddress,
    CoworkingDescription,
    CoworkingPhotoUrl,
    CoworkingCoverUrl,
    TariffId,
    TariffName,
    TariffColor,
    TariffPricePerHour,
    CreatedAt,
)
from infrastructure.database.postgres.models import CoworkingORM, CoworkingTariffORM


class CoworkingDTO(BaseDTO):
    id: CoworkingId
    name: CoworkingName
    address: CoworkingAddress
    photo_url: CoworkingPhotoUrl
    cover_url: CoworkingCoverUrl
    description: Optional[CoworkingDescription] = None
    created_at: CreatedAt

    @classmethod
    def orm_to_dto(cls, orm: CoworkingORM, **kwargs) -> "CoworkingDTO":
        return cls(
            id=orm.id,
            name=orm.name,
            address=orm.address,
            photo_url=orm.photo_url,
            cover_url=orm.cover_url,
            description=orm.description,
            created_at=orm.created_at
        )

    def dto_to_orm(self) -> CoworkingORM:
        return CoworkingORM(
            name=self.name,
            address=self.address,
            photo_url=self.photo_url,
            cover_url=self.cover_url,
            description=self.description,
        )


class CoworkingCreateDTO(BaseDTO):
    name: CoworkingName
    address: CoworkingAddress
    photo_url: CoworkingPhotoUrl
    cover_url: CoworkingCoverUrl
    description: Optional[CoworkingDescription] = None

    def dto_to_orm(self) -> CoworkingORM:
        return CoworkingORM(
            name=self.name,
            address=self.address,
            photo_url=self.photo_url,
            cover_url=self.cover_url,
            description=self.description,
        )

    @classmethod
    def orm_to_dto(cls, orm: CoworkingORM, **kwargs) -> "CoworkingDTO":
        return CoworkingDTO(
            id=orm.id,
            name=orm.name,
            address=orm.address,
            photo_url=orm.photo_url,
            cover_url=orm.cover_url,
            description=orm.description,
            created_at=orm.created_at
        )


class CoworkingUpdateDTO(BaseDTO):
    name: Optional[CoworkingName] = None
    address: Optional[CoworkingAddress] = None
    photo_url: Optional[CoworkingPhotoUrl] = None
    cover_url: Optional[CoworkingCoverUrl] = None
    description: Optional[CoworkingDescription] = None

    @classmethod
    def orm_to_dto(cls, orm: CoworkingORM, **kwargs) -> "CoworkingDTO":
        return CoworkingORM(
            id=orm.id,
            name=orm.name,
            address=orm.address,
            photo_url=orm.photo_url,
            cover_url=orm.cover_url,
            description=orm.description
        )


class CoworkingTariffDTO(BaseDTO):
    id: TariffId
    name: TariffName
    color: TariffColor
    price_per_hour: TariffPricePerHour
    created_at: CreatedAt

    @classmethod
    def orm_to_dto(cls, orm: CoworkingTariffORM, **kwargs) -> "CoworkingTariffDTO":
        return cls(
            id=orm.id,
            name=orm.name,
            color=orm.color,
            price_per_hour=orm.price_per_hour,
            created_at=int(orm.created_at.timestamp()),
        )


class CoworkingTariffCreateDTO(BaseDTO):
    coworking_id: CoworkingId
    name: TariffName
    color: TariffColor
    price_per_hour: TariffPricePerHour

    def dto_to_orm(self) -> CoworkingTariffORM:
        return CoworkingTariffORM(
            coworking_id=self.coworking_id,
            name=self.name,
            color=self.color,
            price_per_hour=self.price_per_hour
        )
