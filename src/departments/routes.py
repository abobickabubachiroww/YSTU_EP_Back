from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from sqlalchemy import select, exists, and_
from typing import Annotated, Any
from src.dependencies import SessionDep
from src.exceptions import (
    DepartmentNotFoundException, DepartmentNameIsNotUniqueException, DepartmentShortNameIsNotUniqueException
)
from .model import Department
from .schemas import DepartmentCreate, DepartmentUpdate, DepartmentRead

router = APIRouter(
    prefix='/departments',
    tags=['departments']
)


@router.get(
    '/{department_id}',
    responses={
        200: {'description': 'Department successfully received'},
        404: {'description': 'Department type not found'}
    },
    summary='Return the department'
)
def get_department(department_id: Annotated[int, Path(gt=0)], session: SessionDep) -> DepartmentRead:
    """Return the department with the specified id"""
    department = session.get(Department, department_id)
    if not department:
        raise DepartmentNotFoundException()
    return department


@router.patch(
    '/{department_id}',
    responses={
        200: {'description': 'Department successfully updated'},
        404: {'description': 'Department not found'},
        409: {'description': 'Department data is not unique'}
    },
    summary='Update the department'
)
def update_department(
        department_id: Annotated[int, Path(gt=0)], department_data: DepartmentUpdate, session: SessionDep
) -> DepartmentRead:
    """Update the department with the specified id with the given information (blank values are ignored)"""
    department = session.get(Department, department_id)
    if not department:
        raise DepartmentNotFoundException()

    if department_data.name:
        stmt = select(exists().where(and_(Department.name == department_data.name, Department.id != department_id)))
        if session.execute(stmt).scalar():
            raise DepartmentNameIsNotUniqueException()

    if department_data.short_name:
        stmt = select(exists().where(
            and_(Department.short_name == department_data.short_name, Department.id != department_id))
        )
        if session.execute(stmt).scalar():
            raise DepartmentShortNameIsNotUniqueException()

    for key, value in department_data.model_dump(exclude_none=True).items():
        setattr(department, key, value)
    session.commit()
    session.refresh(department)
    return department


@router.delete(
    '/{department_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Department successfully deleted'},
        404: {'description': 'Department not found'},
    },
    summary='Delete the department'
)
def delete_department(department_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Response:
    """Delete the department with the specified id."""
    department = session.get(Department, department_id)
    if not department:
        raise DepartmentNotFoundException()
    session.delete(department)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '',
    responses={200: {'description': 'Departments successfully received'}},
    summary='Return a list of departments'
)
def get_departments(session: SessionDep) -> list[DepartmentRead]:
    """Return a list of departments."""
    departments = session.execute(select(Department)).scalars()
    return departments


@router.post(
    '',
    response_model=DepartmentRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Department successfully created'},
        409: {'description': 'Department data is not unique'}
    },
    summary='Create the department'
)
def create_department(department_data: DepartmentCreate, session: SessionDep) -> Any:
    """Create the department with the given information."""
    stmt = select(exists().where(Department.name == department_data.name))
    if session.execute(stmt).scalar():
        raise DepartmentNameIsNotUniqueException()

    stmt = select(exists().where(Department.short_name == department_data.short_name))
    if session.execute(stmt).scalar():
        raise DepartmentShortNameIsNotUniqueException()

    department = Department(**department_data.model_dump())
    session.add(department)
    session.commit()
    session.refresh(department)
    return department
