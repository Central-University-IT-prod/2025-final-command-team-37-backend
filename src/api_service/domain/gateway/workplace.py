from abc import abstractmethod
from typing import Protocol, List

from domain.dto.workplace import WorkplaceUpsertDTO
from domain.dto.misc import CoworkingId
from infrastructure.database.postgres.models import WorkplaceORM


class WorkplaceGateway(Protocol):
    @abstractmethod
    async def upsert_workplaces(self, workplaces: List[WorkplaceUpsertDTO]) -> List[WorkplaceORM]:
        pass

    @abstractmethod
    async def list_workplaces(self, coworking_id: CoworkingId) -> List[WorkplaceORM]:
        pass
