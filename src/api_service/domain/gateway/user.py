from abc import abstractmethod
from typing import Protocol, Optional, List

from domain.dto.misc import TgId
from domain.dto.user import TelegramAuthDTO
from infrastructure.database.postgres.models import UserORM, BookingORM


class UserGateway(Protocol):
    @abstractmethod
    async def get_user(self, tg_id: TgId) -> Optional[UserORM]:
        pass

    @abstractmethod
    async def list_users(self, offset: int, limit: int) -> List[UserORM]:
        pass

    @abstractmethod
    async def add_user(self, user: TelegramAuthDTO) -> None:
        pass
