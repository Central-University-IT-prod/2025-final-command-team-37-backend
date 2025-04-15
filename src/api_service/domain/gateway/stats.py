from abc import abstractmethod
from typing import Protocol


class StatsGateway(Protocol):
    @abstractmethod
    async def get_coworking_count(self) -> int:
        pass

    @abstractmethod
    async def get_workplaces_count(self) -> int:
        pass

    @abstractmethod
    async def get_medium_price_per_hour(self) -> float:
        pass

    @abstractmethod
    async def get_occupancy_rate(self) -> float:
        pass
