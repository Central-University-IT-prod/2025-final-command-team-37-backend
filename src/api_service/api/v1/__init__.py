from fastapi import APIRouter

from .routes import (
    ping,
    user,
    coworking,
    workplace,
    booking,
    stats,
    cdn,
    external,
)

root_router = APIRouter(prefix="/v1")

sub_routers = (
    ping.router,
    user.router,
    coworking.router,
    workplace.router,
    booking.router,
    stats.router,
    cdn.router,
    external.router,
)

for sub_router in sub_routers:
    root_router.include_router(sub_router)
