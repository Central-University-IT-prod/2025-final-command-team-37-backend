from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from infrastructure.database.postgres.session import get_db
from infrastructure.database.repository import (
    UserRepository,
    CoworkingRepository,
    WorkplaceRepository,
    BookingRepository,
    StatsRepository,
)
from domain.gateway import (
    UserGateway,
    CoworkingGateway,
    WorkplaceGateway,
    BookingGateway,
    StatsGateway,
)


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_db_session(self, engine: AsyncEngine) -> AsyncIterable[AsyncSession]:
        async for db_session in get_db(engine):
            yield db_session

    user_gateway = provide(UserRepository, provides=UserGateway)
    coworking_gateway = provide(CoworkingRepository, provides=CoworkingGateway)
    workplace_gateway = provide(WorkplaceRepository, provides=WorkplaceGateway)
    booking_gateway = provide(BookingRepository, provides=BookingGateway)
    stats_gateway = provide(StatsRepository, provides=StatsGateway)
