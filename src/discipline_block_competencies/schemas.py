from typing import Annotated
from pydantic import BaseModel, Field


class DisciplineBlockCompetencyCreate(BaseModel):
    discipline_block_id: Annotated[int, Field(example=1)]
    competency_id: Annotated[int, Field(example=1)]


class DisciplineBlockCompetencyUpdate(BaseModel):
    discipline_block_id: Annotated[int | None, Field(example=1)]
    competency_id: Annotated[int | None, Field(example=1)]


class DisciplineBlockCompetencyRead(DisciplineBlockCompetencyCreate):
    id: Annotated[int, Field(example=1)]
