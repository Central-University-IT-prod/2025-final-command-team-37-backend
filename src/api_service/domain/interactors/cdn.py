import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from core.config import CDNConfig
from core.exceptions import EntityNotFoundError
from domain.dto.cdn import ImageLinkDTO


class SaveImageInteractor:
    def __init__(self, config: CDNConfig):
        self.config = config

    async def __call__(self, file: UploadFile) -> ImageLinkDTO:
        extension = Path(file.filename).suffix
        if extension not in [".png", ".jpg", ".jpeg", ".webp"]:
            raise ValueError("Invalid image data")

        key = str(uuid.uuid4())
        image_path = Path(self.config.STORAGE_PATH) / f"{key}{extension}"

        async with aiofiles.open(image_path, "wb") as f:
            await f.write(await file.read())

        return ImageLinkDTO(id=key, path=f"/api/v1/cdn/file/{key}{extension}").dict()


class GetImageInteractor:
    def __init__(self, config: CDNConfig):
        self.config = config

    async def __call__(self, filename: str) -> Path:
        file_path = Path(self.config.STORAGE_PATH) / filename

        if not file_path.exists():
            raise EntityNotFoundError("File")

        return file_path
