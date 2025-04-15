from typing import List

from core.exceptions import EntityNotFoundError, AccessDeniedError
from domain.gateway.coworking import CoworkingGateway
from domain.dto.coworking import CoworkingDTO, CoworkingCreateDTO, CoworkingUpdateDTO, CoworkingTariffCreateDTO, \
    CoworkingTariffDTO
from domain.dto.misc import CoworkingId


class GetCoworkingInteractor:
    def __init__(self, coworking_gateway: CoworkingGateway):
        self.coworking_gateway = coworking_gateway

    async def __call__(self, coworking_id: CoworkingId) -> CoworkingDTO:
        coworking_orm = await self.coworking_gateway.get_coworking(coworking_id)
        if not coworking_orm:
            raise EntityNotFoundError("Coworking")

        return CoworkingDTO.orm_to_dto(coworking_orm).dict()


class ListCoworkingsInteractor:
    def __init__(self, coworking_gateway: CoworkingGateway):
        self.coworking_gateway = coworking_gateway

    async def __call__(self, offset: int, limit: int) -> List[CoworkingDTO]:
        coworkings = await self.coworking_gateway.list_coworkings(offset, limit)
        return [CoworkingDTO.orm_to_dto(coworking).dict() for coworking in coworkings]


class AddCoworkingInteractor:
    def __init__(self, coworking_gateway: CoworkingGateway):
        self.coworking_gateway = coworking_gateway

    async def __call__(self, coworking: CoworkingCreateDTO, is_admin: bool) -> CoworkingDTO:
        if not is_admin:
            raise AccessDeniedError

        coworking = await self.coworking_gateway.add_coworking(coworking)
        return CoworkingDTO.orm_to_dto(coworking).dict()


class UpdateCoworkingInteractor:
    def __init__(self, coworking_gateway: CoworkingGateway):
        self.coworking_gateway = coworking_gateway

    async def __call__(self, coworking: CoworkingUpdateDTO, coworking_id: CoworkingId, is_admin: bool) -> CoworkingDTO:
        if not is_admin:
            raise AccessDeniedError

        coworking_orm = await self.coworking_gateway.update_coworking(coworking, coworking_id)
        return CoworkingDTO.orm_to_dto(coworking_orm).dict()


class DeleteCoworkingInteractor:
    def __init__(self, coworking_gateway: CoworkingGateway):
        self.coworking_gateway = coworking_gateway

    async def __call__(self, coworking_id: CoworkingId, is_admin: bool) -> None:
        if not is_admin:
            raise AccessDeniedError

        await self.coworking_gateway.delete_coworking(coworking_id)


class AddCoworkingTariffsInteractor:
    def __init__(self, coworking_gateway: CoworkingGateway):
        self.workplace_gateway = coworking_gateway

    async def __call__(self, tariffs: List[CoworkingTariffCreateDTO], is_admin: bool) -> List[CoworkingTariffDTO]:
        if not is_admin:
            raise AccessDeniedError

        workplace_tariffs = await self.workplace_gateway.add_tariffs(tariffs)
        return [CoworkingTariffDTO.orm_to_dto(tariff).dict() for tariff in workplace_tariffs]


class ListCoworkingTariffsInteractor:
    def __init__(self, coworking_gateway: CoworkingGateway):
        self.coworking_gateway = coworking_gateway

    async def __call__(self, coworking_id: CoworkingId) -> List[CoworkingTariffDTO]:
        tariffs = await self.coworking_gateway.list_tariffs(coworking_id)
        return [CoworkingTariffDTO.orm_to_dto(tariff).dict() for tariff in tariffs]
