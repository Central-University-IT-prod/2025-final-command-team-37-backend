from typing import Dict, Any

from .base import BaseDTO
from .misc import (
    WorkplaceId,
    WorkplaceNumber,
    WorkplaceName,
    WorkplaceStatus,
    WorkplaceXCor,
    WorkplaceYCor,
    WorkplaceTags,
    CoworkingId,
    TariffId,
    CreatedAt,
)
from .coworking import CoworkingTariffDTO
from infrastructure.database.postgres.models import WorkplaceORM


class WorkplaceDTO(BaseDTO):
    id: WorkplaceId
    number: WorkplaceNumber
    name: WorkplaceName
    status: WorkplaceStatus
    x_cor: WorkplaceXCor
    y_cor: WorkplaceYCor
    tariff: CoworkingTariffDTO
    created_at: CreatedAt

    @classmethod
    def orm_to_dto(cls, orm: WorkplaceORM, **kwargs) -> "WorkplaceDTO":
        return cls(
            id=orm.id,
            number=orm.number,
            name=orm.name,
            status=orm.status,
            x_cor=orm.x_cor,
            y_cor=orm.y_cor,
            tariff=CoworkingTariffDTO.orm_to_dto(orm.tariff),
            created_at=orm.created_at
        )


class WorkplaceUpsertDTO(BaseDTO):
    coworking_id: CoworkingId
    tariff_id: TariffId
    number: WorkplaceNumber
    name: WorkplaceName
    tags: WorkplaceTags
    x_cor: WorkplaceXCor
    y_cor: WorkplaceYCor

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        return {
            "coworking_id": self.coworking_id,
            "tariff_id": self.tariff_id,
            "number": self.number,
            "name": self.name,
            "tags": self.tags,
            "x_cor": self.x_cor,
            "y_cor": self.y_cor
        }

    def dto_to_orm(self) -> WorkplaceORM:
        return WorkplaceORM(
            coworking_id=self.coworking_id,
            number=self.number,
            name=self.name,
            tags=self.tags,
            x_cor=self.x_cor,
            y_cor=self.y_cor,
            status=WorkplaceStatus.FREE
        )
