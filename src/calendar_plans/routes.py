from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import get_session
from src.dependencies import get_db
from . import repository as repo
from . import schemas
import os, uuid

router = APIRouter(prefix="/calendar-plans", tags=["calendar plans"])



@router.get("", response_model=list[schemas.CalendarPlanOut])
def list_calendar_plans(limit:int=100, offset:int=0, db: Session = Depends(get_db)):
    return repo.list_all(db, limit=limit, offset=offset)

@router.get("/{id}", response_model=schemas.CalendarPlanOut)
def get_calendar_plan(id:int, db: Session = Depends(get_db)):
    obj=repo.get_by_id(db,id)
    if not obj:
        raise HTTPException(status_code=404, detail="Calendar plan not found")
    return obj

@router.post("", response_model=schemas.CalendarPlanOut)
def create_calendar_plan(payload:schemas.CalendarPlanCreate, db: Session = Depends(get_db)):
    data = {"educational_plan_id": payload.educational_plan_id, "data": payload.data}
    return repo.create(db, data)

@router.put("/{id}", response_model=schemas.CalendarPlanOut)
def update_calendar_plan(id:int, payload:schemas.CalendarPlanUpdate, db: Session = Depends(get_db)):
    obj=repo.get_by_id(db,id)
    if not obj:
        raise HTTPException(status_code=404, detail="Calendar plan not found")
    return repo.update(db, obj, {"data": payload.data})

@router.delete("/{id}")
def delete_calendar_plan(id:int, db: Session = Depends(get_db)):
    obj=repo.get_by_id(db,id)
    if not obj:
        raise HTTPException(status_code=404, detail="Calendar plan not found")
    repo.delete(db,obj)
    return {"ok": True}

@router.post("/{id}/upload")
def upload_file(id:int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    obj=repo.get_by_id(db,id)
    if not obj:
        raise HTTPException(status_code=404, detail="Calendar plan not found")
    storage_dir = os.getenv("CALENDAR_STORAGE_DIR", "/tmp/calendar_files")
    os.makedirs(storage_dir, exist_ok=True)
    filename = f"{id}_{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(storage_dir, filename)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return repo.update(db, obj, {"file_path": path})


@router.get("/by-educational-plan/{educational_plan_id}",
            response_model=list[schemas.CalendarPlanOut])
def list_by_educational_plan(
    educational_plan_id: int,
    db: Session = Depends(get_db),
):
    return repo.list_by_educational_plan(db, educational_plan_id)
