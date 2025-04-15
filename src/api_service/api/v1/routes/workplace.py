from typing import Annotated, List

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response, Depends, Query, Body, status
from fastapi.responses import JSONResponse

from api.v1.filters.auth import oauth2_scheme
from core.exceptions import UserUnauthorizedError, AccessDeniedError
from domain.dto.misc import CoworkingId
from domain.interactors.auth import OAuth2PasswordBearerInteractor
from domain.interactors.workplace import (
    UpsertWorkplacesInteractor,
    ListWorkplacesInteractor,
)
from domain.dto.workplace import (
    WorkplaceDTO,
    WorkplaceUpsertDTO,
)

router = APIRouter(route_class=DishkaRoute, prefix="/workplace", tags=["Workplaces"])


@router.post(
    "/upsert",
    response_model=List[WorkplaceDTO],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authenticate",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticate"}
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Access denied",
            "content": {
                "application/json": {
                    "example": {"detail": "Access denied"}
                }
            }
        }
    },
    status_code=status.HTTP_201_CREATED,
)
async def upsert_workplaces(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        workplace_interactor: FromDishka[UpsertWorkplacesInteractor],
        workplaces: List[WorkplaceUpsertDTO] = Body(),
) -> Response:
    try:
        _, is_admin = await auth_interactor(token)
        workplaces = await workplace_interactor(workplaces=workplaces, is_admin=is_admin)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=workplaces,
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail},
        )
    except AccessDeniedError as exc:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.detail},
        )


@router.get(
    "/list",
    response_model=List[WorkplaceDTO],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authenticate",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticate"}
                }
            }
        },
    },
    status_code=status.HTTP_200_OK,
)
async def list_workplaces(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        workplace_interactor: FromDishka[ListWorkplacesInteractor],
        coworking_id: CoworkingId = Query(),
) -> Response:
    try:
        await auth_interactor(token)
        workplaces = await workplace_interactor(coworking_id=coworking_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=workplaces,
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail},
        )
