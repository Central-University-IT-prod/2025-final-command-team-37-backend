from typing import List

from core.exceptions import AccessDeniedError
from domain.gateway import WorkplaceGateway
from domain.dto.misc import CoworkingId
from domain.dto.workplace import WorkplaceUpsertDTO, WorkplaceDTO


class UpsertWorkplacesInteractor:
    def __init__(self, workplace_gateway: WorkplaceGateway):
        self.workplace_gateway = workplace_gateway

    async def __call__(self, workplaces: List[WorkplaceUpsertDTO], is_admin: bool) -> List[WorkplaceDTO]:
        if not is_admin:
            raise AccessDeniedError

        workplaces_orm = await self.workplace_gateway.upsert_workplaces(workplaces)
        return [WorkplaceDTO.orm_to_dto(workplace).dict() for workplace in workplaces_orm]


class ListWorkplacesInteractor:
    def __init__(self, workplace_gateway: WorkplaceGateway):
        self.workplace_gateway = workplace_gateway

    async def __call__(self, coworking_id: CoworkingId) -> List[WorkplaceDTO]:
        workplaces_orm = await self.workplace_gateway.list_workplaces(coworking_id)
        return [WorkplaceDTO.orm_to_dto(workplace).dict() for workplace in workplaces_orm]
