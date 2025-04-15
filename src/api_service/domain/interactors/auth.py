from typing import Tuple
from redis.asyncio import Redis

from core.exceptions import UserUnauthorizedError
from core.security import AuthManager
from infrastructure.database.redis.storage import RedisStorage
from domain.dto.misc import TgId


class GenerateAccessTokenInteractor:
    def __init__(self, auth_manager: AuthManager, redis: Redis):
        self.auth_manager = auth_manager
        self.redis_storage = RedisStorage(redis)

    async def __call__(self, tg_id: TgId) -> str:
        exist_token = await self.redis_storage.get(tg_id)
        if exist_token:
            return exist_token

        token = self.auth_manager.create_access_token({"sub": str(tg_id)})
        ex_time = self.auth_manager.config.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        await self.redis_storage.set(tg_id, token, ex=ex_time)
        return token


class OAuth2PasswordBearerInteractor:
    def __init__(self, auth_manager: AuthManager, redis: Redis):
        self.auth_manager = auth_manager
        self.redis_storage = RedisStorage(redis)

    async def __call__(self, token: str) -> Tuple[int, bool]:
        decoded_token = self.auth_manager.decode_access_token(token)
        if not decoded_token:
            raise UserUnauthorizedError

        sub = decoded_token.get("sub")
        if not sub:
            raise UserUnauthorizedError

        tg_id = int(sub)

        # admins = self.auth_manager.config.TG_ADMINS  # await self.redis_storage.get_list("tg_admins")
        is_admin = True  # tg_id in admins  # sub in admins

        exist_token = await self.redis_storage.get(sub)
        if exist_token != token:
            raise UserUnauthorizedError

        return tg_id, is_admin
