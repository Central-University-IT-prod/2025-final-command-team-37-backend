import os

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response, UploadFile, File, Path, status
from fastapi.responses import JSONResponse, FileResponse

from core.exceptions import EntityNotFoundError
from domain.dto.cdn import ImageLinkDTO
from domain.interactors.cdn import (
    SaveImageInteractor,
    GetImageInteractor,
)

router = APIRouter(route_class=DishkaRoute, prefix="/cdn", tags=["CDN"])


@router.post(
    "/upload",
    response_model=ImageLinkDTO,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Image uploaded",
            "content": {
                "application/json": {
                    "example": {"id": "b1d0d3c1-9a7d-4b7b-9d8f-6e6b1f5b5b8b",
                                "path": "/v1/cdn/file/b1d0d3c1-9a7d-4b7b-9d8f-6e6b1f5b5b8b.jpg"}
                },
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid image data",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid image data"}
                }
            }
        }
    },
    status_code=status.HTTP_201_CREATED,
)
async def upload_image(
        cdn_interactor: FromDishka[SaveImageInteractor],
        file: UploadFile = File()
) -> Response:
    os.makedirs('cdn/storage', exist_ok=True)
    image_link = await cdn_interactor(file)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=image_link,
    )


@router.get(
    "/file/{filename}",
    description="Get file from cdn",
    responses={
        status.HTTP_200_OK: {
            "description": "File found",
            "content": {
                "image/jpeg": {
                    "example": "image/jpeg"
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "File not found",
            "content": {
                "application/json": {
                    "example": {"detail": "File not found"}
                }
            }
        }
    }
)
async def get_image(
        cdn_interactor: FromDishka[GetImageInteractor],
        filename: str = Path()
) -> Response:
    try:
        file_path = await cdn_interactor(filename)
        return FileResponse(file_path)
    except EntityNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.detail},
        )
