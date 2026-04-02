from typing import Annotated
from pydantic import BaseModel, Field


class CompetencyGroupCreate(BaseModel):
    name: Annotated[str, Field(example='Универсальные', max_length=200)]


class CompetencyGroupUpdate(BaseModel):
    name: Annotated[str | None, Field(example='Универсальные', max_length=200)]


class CompetencyGroupRead(CompetencyGroupCreate):
    id: Annotated[int, Field(example=1)]
