from typing import Annotated
from pydantic import BaseModel, Field


class CompetencyCreate(BaseModel):
    code: Annotated[str, Field(example='УК-3', max_length=10)]
    name: Annotated[str, Field(example='Командная работа и лидерство', max_length=30)]
    description: Annotated[str, Field(
        example='Способен осуществлять социальное взаимодействие и реализовывать свою роль в команде.', max_length=255
    )]
    competency_group_id: Annotated[int, Field(gt=0, example=1)]


class CompetencyUpdate(BaseModel):
    code: Annotated[str | None, Field(example='УК-3', max_length=10)]
    name: Annotated[str | None, Field(example='Командная работа и лидерство', max_length=30)]
    description: Annotated[str | None, Field(
        example='Способен осуществлять социальное взаимодействие и реализовывать свою роль в команде.', max_length=255
    )]
    competency_group_id: Annotated[int | None, Field(gt=0, example=1)]


class CompetencyRead(CompetencyCreate):
    id: Annotated[int, Field(example=1)]
