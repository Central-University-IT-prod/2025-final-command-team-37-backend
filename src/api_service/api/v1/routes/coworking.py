from typing import Annotated, List

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response, Depends, Path, Query, Body, status
from fastapi.responses import JSONResponse

from api.v1.filters.auth import oauth2_scheme
from core.exceptions import (
    UserUnauthorizedError,
    AccessDeniedError,
    EntityNotFoundError,
)
from domain.dto.coworking import (
    CoworkingDTO,
    CoworkingCreateDTO,
    CoworkingUpdateDTO,
    CoworkingTariffDTO,
    CoworkingTariffCreateDTO,
)
from domain.dto.misc import CoworkingId
from domain.interactors.auth import OAuth2PasswordBearerInteractor
from domain.interactors.coworking import (
    GetCoworkingInteractor,
    ListCoworkingsInteractor,
    AddCoworkingInteractor,
    UpdateCoworkingInteractor,
    DeleteCoworkingInteractor,
    AddCoworkingTariffsInteractor,
    ListCoworkingTariffsInteractor,
)

router = APIRouter(route_class=DishkaRoute, prefix="/coworking", tags=["Coworking"])


@router.get(
    "/{coworking_id}/get",
    response_model=CoworkingDTO,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authenticate",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticate"}
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Entity not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Entity not found"}
                }
            }
        }
    },
    status_code=status.HTTP_200_OK,
)
async def get_coworking(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        coworking_interactor: FromDishka[GetCoworkingInteractor],
        coworking_id: CoworkingId = Path()
) -> Response:
    try:
        tg_id, _ = await auth_interactor(token)
        coworking = await coworking_interactor(coworking_id=coworking_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=coworking,
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail},
        )
    except EntityNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.detail},
        )


@router.get(
    "/list",
    response_model=List[CoworkingDTO],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authenticate",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticate"}
                }
            }
        }
    },
    status_code=status.HTTP_200_OK,
)
async def list_coworkings(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        coworking_interactor: FromDishka[ListCoworkingsInteractor],
        offset: int = Query(default=0),
        limit: int = Query(default=10)
) -> Response:
    try:
        await auth_interactor(token)
        coworkings = await coworking_interactor(offset=offset, limit=limit)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=coworkings
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail},
        )


@router.post(
    "/add",
    response_model=CoworkingDTO,
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
async def add_coworking(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        coworking_interactor: FromDishka[AddCoworkingInteractor],
        coworking: CoworkingCreateDTO = Body()
) -> Response:
    try:
        _, is_admin = await auth_interactor(token)
        coworking = await coworking_interactor(coworking=coworking, is_admin=is_admin)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=coworking,
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


@router.patch(
    "/{coworking_id}/update",
    response_model=CoworkingDTO,
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
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Entity not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Entity not found"}
                }
            }
        }
    },
    status_code=status.HTTP_200_OK,
)
async def update_coworking(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        coworking_interactor: FromDishka[UpdateCoworkingInteractor],
        coworking_id: CoworkingId = Path(),
        coworking: CoworkingUpdateDTO = Body()
) -> Response:
    try:
        _, is_admin = await auth_interactor(token)
        coworking = await coworking_interactor(coworking=coworking, coworking_id=coworking_id, is_admin=is_admin)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=coworking,
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
    except EntityNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.detail},
        )


@router.delete(
    "/{coworking_id}/delete",
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
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Entity not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Entity not found"}
                }
            }
        }
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_coworking(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        coworking_interactor: FromDishka[DeleteCoworkingInteractor],
        coworking_id: CoworkingId = Path()
) -> Response:
    try:
        _, is_admin = await auth_interactor(token)
        await coworking_interactor(coworking_id=coworking_id, is_admin=is_admin)
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
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
    except EntityNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.detail},
        )


@router.post(
    "/tariffs/add",
    response_model=List[CoworkingTariffDTO],
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
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Entity not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Entity not found"}
                }
            }
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_tariffs(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        coworking_interactor: FromDishka[AddCoworkingTariffsInteractor],
        tariffs: List[CoworkingTariffCreateDTO] = Body(),
) -> Response:
    try:
        _, is_admin = await auth_interactor(token)
        coworking_tariffs = await coworking_interactor(tariffs=tariffs, is_admin=is_admin)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=coworking_tariffs,
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
    except EntityNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.detail},
        )


@router.get(
    "/{coworking_id}/tariffs/list",
    response_model=List[CoworkingTariffDTO],
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
async def list_tariffs(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        coworking_interactor: FromDishka[ListCoworkingTariffsInteractor],
        coworking_id: CoworkingId = Path(),
) -> Response:
    try:
        await auth_interactor(token)
        coworking_tariffs = await coworking_interactor(coworking_id=coworking_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=coworking_tariffs,
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail},
        )
