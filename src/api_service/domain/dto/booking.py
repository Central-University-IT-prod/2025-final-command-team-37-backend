from typing import List, Optional
from .base import BaseDTO
from .misc import (
    TgId,
    WorkplaceId,
    BookingId,
    BookingStartTime,
    BookingEndTime,
    BookingStatus,
    BookingTotalPrice,
    CreatedAt,
)
from .workplace import WorkplaceDTO
from infrastructure.database.postgres.models import BookingORM


class BookingDTO(BaseDTO):
    id: BookingId
    user_id: TgId
    workplaces: List[WorkplaceDTO]
    start_time: BookingStartTime
    end_time: BookingEndTime
    status: BookingStatus
    total_price: BookingTotalPrice
    created_at: CreatedAt

    @classmethod
    def orm_to_dto(cls, booking: BookingORM, **kwargs) -> "BookingDTO":
        return cls(
            id=booking.id,
            user_id=booking.user_id,
            workplaces=[WorkplaceDTO.orm_to_dto(w) for w in booking.workplaces],
            start_time=booking.start_time,
            end_time=booking.end_time,
            status=booking.status,
            total_price=booking.total_price,
            created_at=booking.created_at,
        )


class BookingCreateDTO(BaseDTO):
    workplaces: List[WorkplaceId]
    start_time: BookingStartTime
    end_time: BookingEndTime


class BookingUpdateDTO(BaseDTO):
    start_time: Optional[BookingStartTime] = None
    end_time: Optional[BookingEndTime] = None
