import uuid
from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import (
    String,
    Integer,
    Float,
    BigInteger,
    Enum,
    DateTime,
    ForeignKey,
    Table,
    Column,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import mapped_column, relationship, Mapped

from .base import Base
from domain.dto.misc import UserRole, WorkplaceStatus, BookingStatus

booking_workplaces = Table(
    "booking_workplaces",
    Base.metadata,
    Column("booking_id", UUID(as_uuid=True), ForeignKey("bookings.id"), primary_key=True),
    Column("workplace_id", UUID(as_uuid=True), ForeignKey("workplaces.id"), primary_key=True),
)


class UserORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    photo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    bookings: Mapped[List['BookingORM']] = relationship("BookingORM", back_populates="user",
                                                        cascade="all, delete-orphan")


class CoworkingORM(Base):
    __tablename__ = 'coworkings'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    photo_url: Mapped[str] = mapped_column(String, nullable=False)
    cover_url: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    tariffs: Mapped[List['CoworkingTariffORM']] = relationship("CoworkingTariffORM", back_populates="coworking",
                                                               cascade="all, delete-orphan")
    workplaces: Mapped[List['WorkplaceORM']] = relationship("WorkplaceORM", back_populates="coworking",
                                                            cascade="all, delete-orphan")


class CoworkingTariffORM(Base):
    __tablename__ = 'coworking_tariffs'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    coworking_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("coworkings.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=False)
    price_per_hour: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    coworking: Mapped['CoworkingORM'] = relationship("CoworkingORM", back_populates="tariffs")
    workplaces: Mapped[List['WorkplaceORM']] = relationship("WorkplaceORM", back_populates="tariff")


class WorkplaceORM(Base):
    __tablename__ = 'workplaces'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    coworking_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("coworkings.id"), nullable=False)
    tariff_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("coworking_tariffs.id"), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[WorkplaceStatus] = mapped_column(Enum(WorkplaceStatus), nullable=False, default=WorkplaceStatus.FREE)
    tags: Mapped[List[str]] = mapped_column(MutableList.as_mutable(ARRAY(String)), nullable=True)
    x_cor: Mapped[float] = mapped_column(Float, nullable=False)
    y_cor: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    tariff: Mapped['CoworkingTariffORM'] = relationship("CoworkingTariffORM", back_populates="workplaces")
    coworking: Mapped['CoworkingORM'] = relationship("CoworkingORM", back_populates="workplaces")
    bookings: Mapped[List['BookingORM']] = relationship("BookingORM", secondary=booking_workplaces,
                                                        back_populates="workplaces")


class BookingORM(Base):
    __tablename__ = 'bookings'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    user: Mapped['UserORM'] = relationship("UserORM", back_populates="bookings")
    workplaces: Mapped[List['WorkplaceORM']] = relationship("WorkplaceORM", secondary=booking_workplaces,
                                                            back_populates="bookings")

    @hybrid_property
    def status(self) -> BookingStatus:
        if self.start_time - timedelta(minutes=5) > datetime.now():
            return BookingStatus.WAITING
        elif self.end_time < datetime.now():
            return BookingStatus.FINISHED
        else:
            return BookingStatus.PROCESSING
