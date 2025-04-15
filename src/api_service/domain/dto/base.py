import json
from typing import Dict, Any

from pydantic import BaseModel, ConfigDict, model_validator


class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        return json.loads(self.json(exclude_none=True))

    def dto_to_orm(self, *args, **kwargs) -> Any:
        return None

    @classmethod
    def orm_to_dto(cls, orm: Any, **kwargs) -> "BaseDTO":
        return cls(**dict(orm))

    @model_validator(mode="after")
    def validate_fields(cls, values: "BaseDTO"):
        start_time = getattr(values, "start_time", None)
        end_time = getattr(values, "end_time", None)

        if start_time is not None and end_time is not None and start_time > end_time:
            raise ValueError("start_time must be less than end_time")

        return values
