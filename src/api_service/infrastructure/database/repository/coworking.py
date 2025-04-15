from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from core.exceptions import EntityNotFoundError
from domain.gateway.coworking import CoworkingGateway
from domain.dto.coworking import (
    CoworkingCreateDTO,
    CoworkingUpdateDTO,
    CoworkingTariffCreateDTO,
)
from domain.dto.misc import CoworkingId
from infrastructure.database.postgres.models import CoworkingORM, CoworkingTariffORM


class CoworkingRepository(CoworkingGateway):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_coworking(self, coworking_id: CoworkingId) -> Optional[CoworkingORM]:
        query = select(CoworkingORM).filter(CoworkingORM.id == coworking_id)
        result = await self.db_session.execute(query)
        return result.scalars().one_or_none()

    async def list_coworkings(self, offset: int, limit: int) -> List[CoworkingORM]:
        query = select(CoworkingORM).offset(offset).limit(limit)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def add_coworking(self, coworking: CoworkingCreateDTO) -> CoworkingORM:
        coworking_orm = coworking.dto_to_orm()
        self.db_session.add(coworking_orm)
        await self.db_session.commit()
        await self.db_session.refresh(coworking_orm)

        return coworking_orm

    async def update_coworking(self, coworking: CoworkingUpdateDTO, coworking_id: CoworkingId) -> CoworkingORM:
        coworking_orm = await self.get_coworking(coworking_id)

        if not coworking_orm:
            raise EntityNotFoundError("Coworking")

        if coworking.name:
            coworking_orm.name = coworking.name
        if coworking.address:
            coworking_orm.address = coworking.address
        if coworking.photo_url:
            coworking_orm.photo_url = coworking.photo_url
        if coworking.cover_url:
            coworking_orm.cover_url = coworking.cover_url
        if coworking.description:
            coworking_orm.description = coworking.description

        await self.db_session.commit()
        await self.db_session.refresh(coworking_orm)

        return coworking_orm

    async def delete_coworking(self, coworking_id):
        coworking_orm = await self.get_coworking(coworking_id)
        if not coworking_orm:
            raise EntityNotFoundError("Coworking")

        await self.db_session.delete(coworking_orm)
        await self.db_session.commit()

    async def add_tariffs(self, tariffs: List[CoworkingTariffCreateDTO]) -> List[CoworkingTariffORM]:
        result_rows = []
        for tariff in tariffs:
            tariff_data = tariff.dict()

            coworking_id = tariff_data["coworking_id"]
            coworking_exists = await self.db_session.scalar(
                select(CoworkingORM).where(CoworkingORM.id == coworking_id)
            )
            if coworking_exists is None:
                raise EntityNotFoundError("Coworking")

            update_query = (
                update(CoworkingTariffORM)
                .where(
                    (CoworkingTariffORM.coworking_id == coworking_id) &
                    (CoworkingTariffORM.name == tariff_data["name"])
                )
                .values(**{k: tariff_data[k] for k in tariff_data if k not in ("id", "created_at")})
                .returning(CoworkingTariffORM)
            )
            update_result = await self.db_session.execute(update_query)
            updated_row = update_result.scalar_one_or_none()

            if updated_row:
                result_rows.append(updated_row)
            else:
                insert_query = (
                    insert(CoworkingTariffORM)
                    .values(**tariff_data)
                    .returning(CoworkingTariffORM)
                )
                insert_result = await self.db_session.execute(insert_query)
                inserted_row = insert_result.scalar_one()
                result_rows.append(inserted_row)

        await self.db_session.commit()
        return result_rows

    async def list_tariffs(self, coworking_id: CoworkingId) -> List[CoworkingTariffORM]:
        query = select(CoworkingTariffORM).where(CoworkingTariffORM.coworking_id == coworking_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()
