from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from domain.dto.workplace import WorkplaceUpsertDTO
from domain.gateway.workplace import WorkplaceGateway
from domain.dto.misc import CoworkingId
from infrastructure.database.postgres.models import WorkplaceORM


class WorkplaceRepository(WorkplaceGateway):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def upsert_workplaces(self, workplaces: List[WorkplaceUpsertDTO]) -> List[WorkplaceORM]:
        workplaces_data = [workplace.dict() for workplace in workplaces]

        query = insert(WorkplaceORM).values(workplaces_data)

        update_columns = {
            c.name: getattr(query.excluded, c.name)
            for c in WorkplaceORM.__table__.columns
            if c.name not in ("id", "created_at")
        }

        query = query.on_conflict_do_update(
            index_elements=["id"],
            set_=update_columns
        ).returning(WorkplaceORM)

        result = await self.db_session.execute(query)
        await self.db_session.commit()

        workplaces_result = result.scalars().all()

        workplace_ids = [workplace.id for workplace in workplaces_result]

        query = select(WorkplaceORM).where(WorkplaceORM.id.in_(workplace_ids)).options(
            selectinload(WorkplaceORM.tariff))
        result = await self.db_session.execute(query)
        workplaces_with_tariff = result.scalars().all()

        return workplaces_with_tariff

    async def list_workplaces(self, coworking_id: CoworkingId) -> List[WorkplaceORM]:
        query = select(WorkplaceORM).options(selectinload(WorkplaceORM.tariff)).where(
            WorkplaceORM.coworking_id == coworking_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()
