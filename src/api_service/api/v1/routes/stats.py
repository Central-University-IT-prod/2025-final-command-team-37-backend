from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from domain.interactors.stats import (
    StatsCoworkingCountInteractor,
    StatsWorkplacesCountInteractor,
    StatsMediumPricePerHourInteractor,
    StatsOccupancyRateInteractor,
)

router = APIRouter(route_class=DishkaRoute, prefix="/stats", tags=["Stats"])


@router.get(
    "/coworking-count",
    responses={
        status.HTTP_200_OK: {
            "description": "Returns count of coworkings",
            "content": {
                "application/json": 1
            },
        },
    },
)
async def get_coworking_count(
        stats_interactor: FromDishka[StatsCoworkingCountInteractor]
) -> Response:
    coworking_count = await stats_interactor()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=coworking_count
    )


@router.get(
    "/workplaces-count",
    responses={
        status.HTTP_200_OK: {
            "description": "Returns count of workplaces",
            "content": {
                "application/json": 9
            },
        },
    },
)
async def get_workplaces_count(
        stats_interactor: FromDishka[StatsWorkplacesCountInteractor]
) -> Response:
    workplaces_count = await stats_interactor()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=workplaces_count
    )


@router.get(
    "/medium-price-per-hour",
    responses={
        status.HTTP_200_OK: {
            "description": "Returns medium price per hour",
            "content": {
                "application/json": 7461.42
            },
        },
    },
)
async def get_medium_price_per_hour(
        stats_interactor: FromDishka[StatsMediumPricePerHourInteractor]
) -> Response:
    medium_price_per_hour = await stats_interactor()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=medium_price_per_hour
    )


@router.get(
    "/occupancy-rate",
    responses={
        status.HTTP_200_OK: {
            "description": "Returns occupancy rate",
            "content": {
                "application/json": 7.5
            },
        },
    },
)
async def get_occupancy_rate(
        stats_interactor: FromDishka[StatsOccupancyRateInteractor]
) -> Response:
    occupancy_rate = await stats_interactor()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=occupancy_rate
    )
