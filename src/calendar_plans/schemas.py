
from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class CalendarPlanCreate(BaseModel):
    educational_plan_id: int
    data: dict

class CalendarPlanUpdate(BaseModel):
    data: dict

class CalendarPlanOut(BaseModel):
    id: int
    educational_plan_id: int
    data: dict
    file_path: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
