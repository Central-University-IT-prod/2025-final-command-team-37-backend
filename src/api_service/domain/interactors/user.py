from core.exceptions import EntityNotFoundError
from domain.dto.misc import TgId
from domain.dto.user import UserDTO, TelegramAuthDTO
from domain.gateway import UserGateway


class GetUserInteractor:
    def __init__(self, user_gateway: UserGateway):
        self.user_gateway = user_gateway

    async def __call__(self, tg_id: TgId) -> UserDTO:
        user = await self.user_gateway.get_user(tg_id)
        if not user:
            raise EntityNotFoundError("User")

        return UserDTO.orm_to_dto(user).dict()


class ListUserInteractor:
    def __init__(self, user_gateway: UserGateway):
        self.user_gateway = user_gateway

    async def __call__(self, offset: int, limit: int) -> list[UserDTO]:
        users = await self.user_gateway.list_users(offset=offset, limit=limit)
        return [UserDTO.orm_to_dto(user).dict() for user in users]


class AddUserInteractor:
    def __init__(self, user_gateway: UserGateway):
        self.user_gateway = user_gateway

    async def __call__(self, user: TelegramAuthDTO) -> None:
        # TODO: добавить валидацию auth_date и hash
        await self.user_gateway.add_user(user)
