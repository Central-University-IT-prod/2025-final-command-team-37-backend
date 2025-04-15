from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response, Query, status
from fastapi.responses import JSONResponse

from domain.dto.misc import TgId
from domain.interactors.external import (
    AddTgAdminInteractor,
    RemoveTgAdminInteractor,
)

router = APIRouter(route_class=DishkaRoute, prefix="/external", tags=["External"])


@router.post(
    "/tg_admin/add",
    responses={
        status.HTTP_200_OK: {
            "description": "List of tg admins",
            "content": {
                "application/json": {
                    "example": [1282629807, 1522105862, 5367427116, 946082604, 256086824]
                }
            }
        }
    }
)
async def add_tg_admin(
        external_interactor: FromDishka[AddTgAdminInteractor],
        tg_id: TgId = Query()
) -> Response:
    tg_admins = await external_interactor(tg_id=tg_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=tg_admins
    )


@router.delete(
    "/tg_admin/remove",
    responses={
        status.HTTP_200_OK: {
            "description": "List of tg admins",
            "content": {
                "application/json": {
                    "example": [1282629807, 1522105862, 5367427116, 946082604]
                }
            }
        }
    }
)
async def remove_tg_admin(
        external_interactor: FromDishka[RemoveTgAdminInteractor],
        tg_id: TgId = Query()
) -> Response:
    tg_admins = await external_interactor(tg_id=tg_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=tg_admins
    )
