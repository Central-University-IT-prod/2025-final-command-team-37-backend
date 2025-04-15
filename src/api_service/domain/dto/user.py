from typing import Optional
from random import randint

from .base import BaseDTO
from .misc import (
    TgId,
    FirstName,
    LastName,
    Username,
    AuthDate,
    PhotoUrl,
    UserBalance,
    TgHash,
    UserRole,
    CreatedAt,
)
from infrastructure.database.postgres.models import UserORM


class UserDTO(BaseDTO):
    id: TgId
    first_name: FirstName
    last_name: Optional[LastName] = None
    username: Optional[Username] = None
    photo_url: Optional[PhotoUrl] = None
    balance: UserBalance
    role: UserRole
    created_at: CreatedAt

    @classmethod
    def orm_to_dto(cls, orm: UserORM, **kwargs) -> "UserDTO":
        return cls(
            id=orm.id,
            first_name=orm.first_name,
            last_name=orm.last_name,
            username=orm.username,
            photo_url=orm.photo_url,
            balance=orm.balance,
            role=orm.role,
            created_at=orm.created_at
        )


class TelegramAuthDTO(BaseDTO):
    id: TgId
    first_name: FirstName
    last_name: Optional[LastName] = None
    username: Optional[Username] = None
    photo_url: Optional[PhotoUrl] = None
    auth_date: AuthDate
    hash: TgHash

    def dto_to_orm(self, role: UserRole) -> UserORM:
        user_orm = UserORM(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            photo_url=self.photo_url,
            balance=randint(5, 15) * 1000,  # demo
            role=role
        )

        return user_orm

    @classmethod
    def orm_to_dto(cls, orm: UserORM, **kwargs) -> UserDTO:
        return UserDTO(
            id=orm.id,
            first_name=orm.first_name,
            last_name=orm.last_name,
            username=orm.username,
            photo_url=orm.photo_url,
            balance=orm.balance,
            role=orm.role,
            created_at=orm.created_at
        )
