from typing import Annotated
from pydantic import BaseModel, Field


class MapCoreCreate(BaseModel):
    name: Annotated[str, Field(example='Ядро ЯГТУ', max_length=50)]
    semesters_count: Annotated[int, Field(gt=0, example=8)]


class MapCoreUpdate(BaseModel):
    name: Annotated[str | None, Field(example='Ядро ЯГТУ', max_length=50)]
    semesters_count: Annotated[int | None, Field(gt=0, example=8)]


class MapCoreRead(MapCoreCreate):
    id: Annotated[int, Field(example=1)]
