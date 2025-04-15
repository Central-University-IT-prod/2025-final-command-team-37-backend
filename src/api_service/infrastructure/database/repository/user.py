from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import EntityNotFoundError
from core.config import SecurityConfig
from domain.gateway import UserGateway
from domain.dto.user import TelegramAuthDTO
from domain.dto.misc import TgId, UserRole
from infrastructure.database.postgres.models import UserORM, BookingORM


class UserRepository(UserGateway):
    def __init__(self, db_session: AsyncSession, config: SecurityConfig):
        self.db_session = db_session
        self.config = config

    async def get_user(self, tg_id: TgId) -> Optional[UserORM]:
        query = select(UserORM).where(UserORM.id == tg_id)
        result = await self.db_session.execute(query)
        return result.scalars().one_or_none()

    async def list_users(self, offset: int, limit: int) -> List[UserORM]:
        query = select(UserORM).offset(offset).limit(limit)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def add_user(self, user: TelegramAuthDTO) -> None:
        exist_user = await self.get_user(user.id)

        # role = UserRole.ADMIN if user.id in self.config.TG_ADMINS else UserRole.USER
        role = UserRole.ADMIN
        if exist_user:
            exist_user.id = user.id
            exist_user.first_name = user.first_name
            exist_user.last_name = user.last_name
            exist_user.username = user.username
            exist_user.photo_url = user.photo_url
            exist_user.role = role

            await self.db_session.commit()
            await self.db_session.refresh(exist_user)

            return

        new_user = user.dto_to_orm(role=role)

        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)

    async def delete_user(self, tg_id: TgId) -> None:
        user = await self.get_user(tg_id)
        if not user:
            raise EntityNotFoundError

        await self.db_session.delete(user)
        await self.db_session.commit()

    async def list_user_bookings(self, tg_id: TgId, offset: int, limit: int) -> List[BookingORM]:
        query = (
            select(BookingORM)
            .options(selectinload(BookingORM.workplace))
            .where(BookingORM.user_id == tg_id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.db_session.execute(query)
        return result.scalars().all()
