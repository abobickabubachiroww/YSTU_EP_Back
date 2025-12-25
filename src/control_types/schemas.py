from typing import Annotated
from pydantic import BaseModel, Field


class ControlTypeCreate(BaseModel):
    name: Annotated[str, Field(example='Дифференцированный зачет', max_length=30)]


class ControlTypeUpdate(BaseModel):
    name: Annotated[str | None, Field(example='Дифференцированный зачет', max_length=30)]


class ControlTypeRead(ControlTypeCreate):
    id: Annotated[int, Field(example=1)]
