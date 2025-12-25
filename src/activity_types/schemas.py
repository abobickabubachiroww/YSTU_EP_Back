from typing import Annotated
from pydantic import BaseModel, Field


class ActivityTypeCreate(BaseModel):
    name: Annotated[str, Field(example='Практическое занятие', max_length=30)]


class ActivityTypeUpdate(BaseModel):
    name: Annotated[str | None, Field(example='Практическое занятие', max_length=30)]


class ActivityTypeRead(ActivityTypeCreate):
    id: Annotated[int, Field(example=1)]
