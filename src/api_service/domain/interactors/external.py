from typing import List

from core.config import SecurityConfig
from domain.dto.misc import TgId


class AddTgAdminInteractor:
    def __init__(self, config: SecurityConfig):
        self.config = config

    async def __call__(self, tg_id: TgId) -> List[int]:
        if tg_id not in self.config.TG_ADMINS:
            self.config.TG_ADMINS.append(tg_id)

        return self.config.TG_ADMINS


class RemoveTgAdminInteractor:
    def __init__(self, config: SecurityConfig):
        self.config = config

    async def __call__(self, tg_id: TgId) -> List[int]:
        if tg_id in self.config.TG_ADMINS:
            self.config.TG_ADMINS.remove(tg_id)

        return self.config.TG_ADMINS
