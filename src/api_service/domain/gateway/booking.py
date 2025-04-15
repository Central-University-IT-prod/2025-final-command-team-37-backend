from abc import abstractmethod
from typing import Protocol, List

from domain.dto.booking import BookingCreateDTO, BookingUpdateDTO
from domain.dto.misc import TgId, CoworkingId, BookingId
from infrastructure.database.postgres.models import BookingORM


class BookingGateway(Protocol):
    @abstractmethod
    async def get_booking(self, booking_id: BookingId) -> BookingORM:
        pass

    @abstractmethod
    async def list_user_bookings(self, tg_id: TgId) -> List[BookingORM]:
        pass

    @abstractmethod
    async def list_coworking_bookings(self, coworking_id: CoworkingId) -> List[BookingORM]:
        pass

    @abstractmethod
    async def list_all_bookings(self) -> List[BookingORM]:
        pass

    @abstractmethod
    async def add_booking(self, booking: BookingCreateDTO, user_id: TgId) -> BookingORM:
        pass

    @abstractmethod
    async def update_booking(self, booking: BookingUpdateDTO, booking_id: BookingId, user_id: TgId) -> BookingORM:
        pass

    @abstractmethod
    async def delete_booking(self, booking_id: BookingId, user_id: TgId) -> None:
        pass

    @abstractmethod
    async def activate_booking(self, booking_id: BookingId, user_id: TgId) -> None:
        pass

    @abstractmethod
    async def pending_bookings(self) -> List[BookingORM]:
        pass
