from typing import Annotated, List, Optional

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response, Query, Body, status, Depends
from fastapi.responses import JSONResponse

from api.v1.filters.auth import oauth2_scheme
from core.exceptions import UserUnauthorizedError, EntityNotFoundError, AccessDeniedError
from domain.dto.booking import BookingDTO, BookingCreateDTO
from domain.dto.misc import TgId, CoworkingId, BookingId
from domain.interactors.auth import OAuth2PasswordBearerInteractor
from domain.interactors.booking import (
    GetBookingInteractor,
    ListUserBookingsInteractor,
    ListCoworkingBookingsInteractor,
    ListAllBookingsInteractor,
    AddBookingInteractor,
    UpdateBookingInteractor,
    DeleteBookingInteractor,
    ActivateBookingInteractor,
    PendingBookingsInteractor,
)

router = APIRouter(route_class=DishkaRoute, prefix="/bookings", tags=["Booking"])


@router.get(
    "/get",
    response_model=BookingDTO,
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
            "description": "Booking not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Booking not found"}
                }
            }
        },
    },
    status_code=status.HTTP_200_OK,
)
async def get_booking(
        token: Annotated[str, Depends(oauth2_scheme)],
        oauth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        booking_interactor: FromDishka[GetBookingInteractor],
        booking_id: BookingId = Query()
) -> Response:
    try:
        tg_id, _ = await oauth_interactor(token)
        booking = await booking_interactor(booking_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=booking,
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
    "/list/user",
    response_model=List[BookingDTO],
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
    },
    status_code=status.HTTP_200_OK,
)
async def list_user_bookings(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        booking_interactor: FromDishka[ListUserBookingsInteractor],
        user_id: Optional[TgId] = Query(default=None)
) -> Response:
    try:
        tg_id, is_admin = await auth_interactor(token)
        admin = False
        if user_id:
            tg_id = user_id
            admin = True
        user_bookings = await booking_interactor(tg_id=tg_id, admin=admin,
                                                 is_admin=is_admin)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=user_bookings,
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail},
        )
    except AccessDeniedError as exc:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.detail}
        )


@router.get(
    "/list/coworking",
    response_model=List[BookingDTO],
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
            "description": "Coworking not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Coworking not found"}
                }
            }
        },
    },
    status_code=status.HTTP_200_OK,
)
async def list_coworking_bookings(
        token: Annotated[str, Depends(oauth2_scheme)],
        oauth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        booking_interactor: FromDishka[ListCoworkingBookingsInteractor],
        coworking_id: CoworkingId = Query()
) -> Response:
    try:
        tg_id, _ = await oauth_interactor(token)
        user_bookings = await booking_interactor(coworking_id=coworking_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=user_bookings,
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
    "/list/all",
    response_model=List[BookingDTO],
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
    },
    status_code=status.HTTP_200_OK,
)
async def get_all_bookings(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        booking_interactor: FromDishka[ListAllBookingsInteractor],
) -> Response:
    try:
        tg_id, is_admin = await auth_interactor(token)
        all_bookings = await booking_interactor(is_admin=is_admin)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=all_bookings,
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail},
        )
    except AccessDeniedError as exc:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.detail}
        )


@router.post(
    "/add",
    response_model=BookingDTO,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {"detail": "Unauthorized"}
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
            "description": "Booking not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Booking not found"}
                }
            }
        }
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_bookings(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        booking_interactor: FromDishka[AddBookingInteractor],
        data: BookingCreateDTO = Body()
) -> Response:
    try:
        tg_id, _ = await auth_interactor(token)
        bookings = await booking_interactor(data, tg_id)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=bookings.dict(),
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail}
        )
    except AccessDeniedError as exc:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.detail}
        )
    except EntityNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.detail}
        )


@router.patch(
    "/update",
    response_model=BookingDTO,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {"detail": "Unauthorized"}
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Booking is not waiting",
            "content": {
                "application/json": {
                    "example": {"detail": "Booking is not waiting"}
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Booking not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Booking not found"}
                }
            }
        }
    },
    status_code=status.HTTP_200_OK,
)
async def update_bookings(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        booking_interactor: FromDishka[UpdateBookingInteractor],
        data: BookingCreateDTO = Body(),
        booking_id: BookingId = Query()
) -> Response:
    try:
        tg_id, _ = await auth_interactor(token)
        bookings = await booking_interactor(data, booking_id, tg_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=bookings.dict(),
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail}
        )
    except AccessDeniedError as exc:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.detail}
        )
    except EntityNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.detail}
        )


@router.delete(
    "/delete",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {"detail": "Unauthorized"}
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
            "description": "Booking not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Booking not found"}
                }
            }
        }
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bookings(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_interactor: FromDishka[OAuth2PasswordBearerInteractor],
        booking_interactor: FromDishka[DeleteBookingInteractor],
        booking_id: TgId = Query()
) -> Response:
    try:
        tg_id, _ = await auth_interactor(token)
        await booking_interactor(booking_id, tg_id)
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail}
        )
    except AccessDeniedError as exc:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.detail}
        )
    except EntityNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.detail}
        )


@router.post(
    "/activate",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {"detail": "Unauthorized"}
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
            "description": "Booking not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Booking not found"}
                }
            }
        }
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def activate_booking(
        booking_interactor: FromDishka[ActivateBookingInteractor],
        booking_id: BookingId = Query(),
        user_id: TgId = Query()
) -> Response:
    try:
        await booking_interactor(booking_id, user_id)
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
        )
    except UserUnauthorizedError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.detail}
        )
    except AccessDeniedError as exc:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.detail}
        )
    except EntityNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.detail}
        )


@router.get(
    "/pending",
    response_model=List[BookingDTO],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {"detail": "Unauthorized"}
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
    },
    status_code=status.HTTP_200_OK,
)
async def pending_bookings(
        booking_interactor: FromDishka[PendingBookingsInteractor]
) -> Response:
    bookings = await booking_interactor()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=bookings
    )
