from typing import List
from datetime import timedelta

from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import EntityNotFoundError, AccessDeniedError
from domain.dto.booking import BookingCreateDTO, BookingUpdateDTO
from domain.dto.misc import TgId, BookingId, BookingStatus, CoworkingId
from domain.gateway.booking import BookingGateway
from infrastructure.database.postgres.models import CoworkingORM, WorkplaceORM, BookingORM, booking_workplaces


class BookingRepository(BookingGateway):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_booking(self, booking_id: BookingId) -> BookingORM:
        query = select(BookingORM).options(selectinload(BookingORM.workplaces)).where(BookingORM.id == booking_id)
        result = await self.db_session.execute(query)
        booking = result.scalars().one_or_none()
        if not booking:
            raise EntityNotFoundError("Booking")

        return booking

    async def list_user_bookings(self, tg_id: TgId) -> List[BookingORM]:
        query = select(BookingORM).options(selectinload(BookingORM.workplaces)).where(BookingORM.user_id == tg_id)
        result = await self.db_session.execute(query)
        bookings = result.scalars().all()

        return bookings

    async def list_coworking_bookings(self, coworking_id: CoworkingId) -> List[BookingORM]:
        coworking_query = select(CoworkingORM).where(CoworkingORM.id == coworking_id)
        coworking_result = await self.db_session.execute(coworking_query)
        coworking = coworking_result.scalars().one_or_none()
        if not coworking:
            raise EntityNotFoundError("Coworking")

        query = (
            select(BookingORM)
            .options(selectinload(BookingORM.workplaces).selectinload(WorkplaceORM.tariff))
            .join(booking_workplaces)
            .join(WorkplaceORM)
            .where(WorkplaceORM.coworking_id == coworking_id)
        )
        result = await self.db_session.execute(query)
        bookings = result.scalars().all()
        return bookings

    async def list_all_bookings(self) -> List[BookingORM]:
        query = select(BookingORM).options(selectinload(BookingORM.workplaces))
        result = await self.db_session.execute(query)
        bookings = result.scalars().all()

        return bookings

    async def add_booking(self, booking: BookingCreateDTO, user_id: TgId) -> BookingORM:
        query = (
            select(WorkplaceORM)
            .options(selectinload(WorkplaceORM.tariff))
            .where(WorkplaceORM.id.in_(booking.workplaces))
        )
        result = await self.db_session.execute(query)
        workplaces = result.scalars().all()

        if not workplaces:
            raise EntityNotFoundError("Workplaces")

        conflict_query = (
            select(BookingORM)
            .join(booking_workplaces)
            .where(
                booking_workplaces.c.workplace_id.in_(booking.workplaces),
                BookingORM.start_time < booking.end_time,
                BookingORM.end_time > booking.start_time,
            )
        )
        conflict_result = await self.db_session.execute(conflict_query)
        conflict = conflict_result.scalars().one_or_none()
        if conflict:
            raise AccessDeniedError("Workplace is already booked")

        duration_hours = (booking.end_time - booking.start_time).total_seconds() / 3600
        total_price = sum(w.tariff.price_per_hour * duration_hours for w in workplaces)

        new_booking = BookingORM(
            user_id=user_id,
            start_time=booking.start_time,
            end_time=booking.end_time,
            total_price=total_price,
        )
        new_booking.workplaces = workplaces

        self.db_session.add(new_booking)
        await self.db_session.commit()

        return new_booking

    async def update_booking(self, booking: BookingUpdateDTO, booking_id: BookingId, user_id: TgId) -> BookingORM:
        query = (
            select(BookingORM)
            .where(
                and_(
                    BookingORM.id == booking_id,
                    BookingORM.user_id == user_id,
                )
            )
        )
        result = await self.db_session.execute(query)
        booking_orm = result.scalars().one_or_none()
        if not booking_orm:
            raise EntityNotFoundError("Booking")

        if booking_orm.status != BookingStatus.WAITING:
            raise AccessDeniedError("Booking is not waiting")

        if booking.start_time is not None:
            booking_orm.start_time = booking.start_time
        if booking.end_time is not None:
            booking_orm.end_time = booking.end_time

        duration_hours = (booking.end_time - booking.start_time).total_seconds() / 3600
        booking_orm.total_price = sum(w.tariff.price_per_hour * duration_hours for w in booking_orm.workplaces)

        await self.db_session.commit()
        await self.db_session.refresh(booking_orm)

        return booking_orm

    async def delete_booking(self, booking_id: BookingId, user_id: TgId) -> None:
        query = (
            select(BookingORM)
            .where(
                and_(
                    BookingORM.id == booking_id,
                    BookingORM.user_id == user_id,
                )
            )
        )
        result = await self.db_session.execute(query)
        booking_orm = result.scalars().one_or_none()
        if not booking_orm:
            raise EntityNotFoundError("Booking")

        await self.db_session.delete(booking_orm)
        await self.db_session.commit()

    async def activate_booking(self, booking_id: BookingId, user_id: TgId) -> None:
        query = select(BookingORM).where(
            and_(
                BookingORM.id == booking_id,
                BookingORM.user_id == user_id,
            )
        )
        result = await self.db_session.execute(query)
        booking = result.scalars().one_or_none()
        if not booking:
            raise EntityNotFoundError("Booking")

        if BookingORM.status != BookingStatus.PROCESSING:
            raise AccessDeniedError

    async def pending_bookings(self) -> List[BookingORM]:
        # остался час до начала
        query = select(BookingORM).where(BookingORM.start_time - timedelta(seconds=3600) < BookingORM.end_time)
        result = await self.db_session.execute(query)
        return result.scalars().all()
