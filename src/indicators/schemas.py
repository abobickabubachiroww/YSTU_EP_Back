from typing import Annotated
from pydantic import BaseModel, Field


class IndicatorCreate(BaseModel):
    code: Annotated[str, Field(example='УК-1.1', max_length=10)]
    name: Annotated[str, Field(example='Знать: методики поиска, сбора и обработки информации; актуальные российские и '
                                       'зарубежные источники информации в сфере профессиональной деятельности; '
                                       'метод системного анализа.', max_length=255)]
    competency_id: Annotated[int, Field(gt=0, example=1)]


class IndicatorUpdate(BaseModel):
    code: Annotated[str | None, Field(example='УК-1.1', max_length=10)]
    name: Annotated[str | None, Field(example='Знать: методики поиска, сбора и обработки информации; актуальные '
                                              'российские и зарубежные источники информации в сфере профессиональной '
                                              'деятельности; метод системного анализа.', max_length=255)]
    competency_id: Annotated[int | None, Field(gt=0, example=1)]


class IndicatorRead(IndicatorCreate):
    id: Annotated[int, Field(example=1)]
