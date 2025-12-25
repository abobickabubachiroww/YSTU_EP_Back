from typing import Annotated
from pydantic import BaseModel, Field


class CompetencyGroupCreate(BaseModel):
    name: Annotated[str, Field(example='Универсальные', max_length=30)]


class CompetencyGroupUpdate(BaseModel):
    name: Annotated[str | None, Field(example='Универсальные', max_length=30)]


class CompetencyGroupRead(CompetencyGroupCreate):
    id: Annotated[int, Field(example=1)]
