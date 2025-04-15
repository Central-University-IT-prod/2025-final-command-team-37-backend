from typing import Annotated, List

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response, Depends, Query, Body, status
from fastapi.responses import JSONResponse

from api.v1.filters.auth import oauth2_scheme
from core.exceptions import (
    EntityNotFoundError,
    UserUnauthorizedError,
)
from domain.dto.user import UserDTO, TelegramAuthDTO
from domain.interactors.auth import (
    GenerateAccessTokenInteractor,
    OAuth2PasswordBearerInteractor,
)
from domain.interactors.user import (
    GetUserInteractor,
    ListUserInteractor,
    AddUserInteractor,
)

router = APIRouter(route_class=DishkaRoute, prefix="/user", tags=["User"])


@router.get(
    "/profile",
    response_model=UserDTO,
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
async def get_profile(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        user_interactor: FromDishka[GetUserInteractor]
) -> Response:
    try:
        tg_id, _ = await auth_interactor(token)
        user = await user_interactor(tg_id=tg_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=user,
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
    response_model=List[UserDTO],
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
async def list_users(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        user_interactor: FromDishka[ListUserInteractor],
        offset: int = Query(default=0),
        limit: int = Query(default=10)
) -> Response:
    try:
        await auth_interactor(token)
        users = await user_interactor(offset=offset, limit=limit)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=users,
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail},
        )


@router.post(
    "/auth",
    response_model=None,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {"token": "REDACTED"}
                }
            }
        },
    },
)
async def auth_user(
        auth_interactor: FromDishka[GenerateAccessTokenInteractor],
        user_interactor: FromDishka[AddUserInteractor],
        user: TelegramAuthDTO = Body()
) -> Response:
    await user_interactor(user=user)
    token = await auth_interactor(tg_id=user.id)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"token": token},
    )
