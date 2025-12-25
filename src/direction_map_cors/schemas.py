from typing import Annotated
from pydantic import BaseModel, Field


class DirectionMapCoreCreate(BaseModel):
    direction_id: Annotated[int, Field(example=1)]
    map_core_id: Annotated[int, Field(example=1)]


class DirectionMapCoreUpdate(BaseModel):
    direction_id: Annotated[int | None, Field(example=1)]
    map_core_id: Annotated[int | None, Field(example=1)]


class DirectionMapCoreRead(DirectionMapCoreCreate):
    id: Annotated[int, Field(example=1)]
