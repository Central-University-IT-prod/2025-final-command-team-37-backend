from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from domain.gateway import StatsGateway
from domain.dto.misc import WorkplaceStatus
from infrastructure.database.postgres.models import CoworkingORM, CoworkingTariffORM, WorkplaceORM


class StatsRepository(StatsGateway):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_coworking_count(self) -> int:
        query = select(func.count(CoworkingORM.id))
        result = await self.db_session.execute(query)
        return result.scalar()

    async def get_workplaces_count(self) -> int:
        query = select(func.count(WorkplaceORM.id))
        result = await self.db_session.execute(query)
        return result.scalar()

    async def get_medium_price_per_hour(self) -> float:
        query = (
            select(func.avg(CoworkingTariffORM.price_per_hour))
            .select_from(WorkplaceORM)
            .join(CoworkingTariffORM, WorkplaceORM.tariff)
        )
        result = await self.db_session.execute(query)
        return result.scalar()

    async def get_occupancy_rate(self) -> float:
        total_query = select(func.count(WorkplaceORM.id))
        total_result = await self.db_session.execute(total_query)
        total_count = total_result.scalar() or 0

        if total_count == 0:
            return 0.0

        occupied_query = (
            select(func.count(WorkplaceORM.id))
            .where(WorkplaceORM.status != WorkplaceStatus.FREE)
        )
        occupied_result = await self.db_session.execute(occupied_query)
        occupied_count = occupied_result.scalar() or 0

        return occupied_count / total_count
