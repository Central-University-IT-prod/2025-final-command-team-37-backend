from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Ping"])


@router.get(
    "/ping",
    responses={
        status.HTTP_200_OK: {
            "description": "Ping",
            "content": {
                "application/json": {
                    "example": {"ping": "pong-pong-pong"}
                }
            }
        }
    }
)
async def ping() -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"ping": "pong-pong-pong"}
    )
