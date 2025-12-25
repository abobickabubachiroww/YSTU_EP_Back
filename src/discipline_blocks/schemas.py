from typing import Annotated
from pydantic import BaseModel, Field


class DisciplineBlockCreate(BaseModel):
    discipline_id: Annotated[int, Field(example=1)]
    credit_units: Annotated[int, Field(example=3)]
    control_type_id: Annotated[int, Field(example=1)]
    lecture_hours: Annotated[int, Field(example=40)]
    practice_hours: Annotated[int, Field(example=40)]
    lab_hours: Annotated[int, Field(example=40)]
    semester_number: Annotated[int, Field(example=3)]
    map_core_id: Annotated[int, Field(example=1)]


class DisciplineBlockUpdate(BaseModel):
    discipline_id: Annotated[int | None, Field(example=1)]
    credit_units: Annotated[int | None, Field(example=3)]
    control_type_id: Annotated[int | None, Field(example=1)]
    lecture_hours: Annotated[int | None, Field(example=40)]
    practice_hours: Annotated[int | None, Field(example=40)]
    lab_hours: Annotated[int | None, Field(example=40)]
    semester_number: Annotated[int | None, Field(example=3)]
    map_core_id: Annotated[int | None, Field(example=1)]


class DisciplineBlockRead(DisciplineBlockCreate):
    id: Annotated[int, Field(example=1)]
