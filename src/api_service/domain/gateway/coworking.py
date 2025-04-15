from abc import abstractmethod
from typing import Protocol, Optional, List

from domain.dto.coworking import CoworkingCreateDTO, CoworkingUpdateDTO, CoworkingTariffCreateDTO
from domain.dto.misc import CoworkingId
from infrastructure.database.postgres.models import CoworkingORM, CoworkingTariffORM


class CoworkingGateway(Protocol):
    @abstractmethod
    async def get_coworking(self, coworking_id: CoworkingId) -> Optional[CoworkingORM]:
        pass

    @abstractmethod
    async def list_coworkings(self, offset: int, limit: int) -> List[CoworkingORM]:
        pass

    @abstractmethod
    async def add_coworking(self, coworking: CoworkingCreateDTO) -> CoworkingORM:
        pass

    @abstractmethod
    async def update_coworking(self, coworking: CoworkingUpdateDTO, coworking_id: CoworkingId) -> CoworkingORM:
        pass

    @abstractmethod
    async def delete_coworking(self, coworking_id: CoworkingId) -> None:
        pass

    @abstractmethod
    async def add_tariffs(self, tariff: List[CoworkingTariffCreateDTO]) -> List[CoworkingTariffORM]:
        pass

    @abstractmethod
    async def list_tariffs(self, coworking_id: CoworkingId) -> List[CoworkingTariffORM]:
        pass
