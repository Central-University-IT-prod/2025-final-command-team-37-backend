from typing import Any, List

from redis.asyncio import Redis


class RedisStorage:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def set(self, key: str, value: str, ex=None) -> None:
        await self.redis.set(key, value, ex=ex)

    async def get(self, key: str, default=None) -> Any:
        return await self.redis.get(key) or default

    async def add_to_list(self, key: str, value: str) -> None:
        await self.redis.rpush(key, value)

    async def get_list(self, key: str) -> List[str]:
        return await self.redis.lrange(key, 0, -1)
