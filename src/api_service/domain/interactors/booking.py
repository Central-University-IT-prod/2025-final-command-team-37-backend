from typing import List

from core.exceptions import AccessDeniedError
from domain.gateway.booking import BookingGateway
from domain.dto.misc import TgId, CoworkingId, BookingId
from domain.dto.booking import BookingDTO, BookingCreateDTO


class GetBookingInteractor:
    def __init__(self, booking_gateway: BookingGateway):
        self.booking_gateway = booking_gateway

    async def __call__(self, booking_id: TgId) -> BookingDTO:
        booking_orm = await self.booking_gateway.get_booking(booking_id)
        return BookingDTO.orm_to_dto(booking_orm).dict()


class ListUserBookingsInteractor:
    def __init__(self, booking_gateway: BookingGateway):
        self.booking_gateway = booking_gateway

    async def __call__(self, tg_id: TgId, admin: bool, is_admin: bool) -> List[BookingDTO]:
        if admin and not is_admin:
            raise AccessDeniedError

        user_bookings = await self.booking_gateway.list_user_bookings(tg_id=tg_id)
        return [BookingDTO.orm_to_dto(booking).dict() for booking in user_bookings]


class ListCoworkingBookingsInteractor:
    def __init__(self, booking_gateway: BookingGateway):
        self.booking_gateway = booking_gateway

    async def __call__(self, coworking_id: CoworkingId) -> List[BookingDTO]:
        coworking_bookings = await self.booking_gateway.list_coworking_bookings(coworking_id)
        return [BookingDTO.orm_to_dto(booking).dict() for booking in coworking_bookings]


class ListAllBookingsInteractor:
    def __init__(self, booking_gateway: BookingGateway):
        self.booking_gateway = booking_gateway

    async def __call__(self, is_admin: bool) -> List[BookingDTO]:
        if not is_admin:
            raise AccessDeniedError

        all_bookings = await self.booking_gateway.list_all_bookings()
        return [BookingDTO.orm_to_dto(booking).dict() for booking in all_bookings]


class AddBookingInteractor:
    def __init__(self, booking_gateway: BookingGateway):
        self.booking_gateway = booking_gateway

    async def __call__(self, booking: BookingCreateDTO, user_id: TgId) -> BookingDTO:
        booking_orm = await self.booking_gateway.add_booking(booking, user_id)
        return BookingDTO.orm_to_dto(booking_orm)


class UpdateBookingInteractor:
    def __init__(self, booking_gateway: BookingGateway):
        self.booking_gateway = booking_gateway

    async def __call__(self, booking: BookingCreateDTO, booking_id: BookingId, user_id: TgId) -> BookingDTO:
        booking_orm = await self.booking_gateway.update_booking(booking, booking_id, user_id)
        return BookingDTO.orm_to_dto(booking_orm)


class DeleteBookingInteractor:
    def __init__(self, booking_gateway: BookingGateway):
        self.booking_gateway = booking_gateway

    async def __call__(self, booking_id: TgId, user_id: TgId) -> None:
        await self.booking_gateway.delete_booking(booking_id, user_id)


class ActivateBookingInteractor:
    def __init__(self, booking_gateway: BookingGateway):
        self.booking_gateway = booking_gateway

    async def __call__(self, booking_id: BookingId, user_id: TgId) -> None:
        await self.booking_gateway.activate_booking(booking_id, user_id)


class PendingBookingsInteractor:
    def __init__(self, booking_gateway: BookingGateway):
        self.booking_gateway = booking_gateway

    async def __call__(self) -> List[BookingDTO]:
        bookings_orm = await self.booking_gateway.pending_bookings()
        return [BookingDTO.orm_to_dto(booking).dict() for booking in bookings_orm]
