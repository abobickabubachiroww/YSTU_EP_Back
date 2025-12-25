from typing import Annotated
from pydantic import BaseModel, Field


class DisciplineCreate(BaseModel):
    name: Annotated[str, Field(example='Проектный практикум', max_length=255)]
    short_name: Annotated[str, Field(example="ПП", max_length=50)]
    department_id: Annotated[int, Field(example=1)]


class DisciplineUpdate(BaseModel):
    name: Annotated[str | None, Field(example='Проектный практикум', max_length=255)]
    short_name: Annotated[str | None, Field(example="ПП", max_length=50)]
    department_id: Annotated[int, Field(example=1)]


class DisciplineRead(DisciplineCreate):
    id: Annotated[int, Field(example=1)]
