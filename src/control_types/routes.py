from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from sqlalchemy import select, exists, and_
from typing import Annotated, Any
from src.dependencies import SessionDep
from src.exceptions import ControlTypeNotFoundException, ControlTypeNameIsNotUniqueException
from .model import ControlType
from .schemas import ControlTypeCreate, ControlTypeUpdate, ControlTypeRead

router = APIRouter(
    prefix='/control-types',
    tags=['control types']
)


@router.get(
    '/{control_type_id}',
    responses={
        200: {'description': 'Control type successfully received'},
        404: {'description': 'Control type not found'}
    },
    summary='Return the control type'
)
def get_control_type(control_type_id: Annotated[int, Path(gt=0)], session: SessionDep) -> ControlTypeRead:
    """Return the control type with the specified id"""
    control_type = session.get(ControlType, control_type_id)
    if not control_type:
        raise ControlTypeNotFoundException()
    return control_type


@router.patch(
    '/{control_type_id}',
    responses={
        200: {'description': 'Control type successfully updated'},
        404: {'description': 'Control type not found'},
        409: {'description': 'Control type data is not unique'}
    },
    summary='Update the control type'
)
def update_control_type(
        control_type_id: Annotated[int, Path(gt=0)], control_type_data: ControlTypeUpdate, session: SessionDep
) -> ControlTypeRead:
    """Update the control type with the specified id with the given information (blank values are ignored)"""
    control_type = session.get(ControlType, control_type_id)
    if not control_type:
        raise ControlTypeNotFoundException()

    if control_type_data.name:
        stmt = select(exists().where(and_(
            ControlType.name == control_type_data.name, ControlType.id != control_type_id
        )))
        if session.execute(stmt).scalar():
            raise ControlTypeNameIsNotUniqueException()

    for key, value in control_type_data.model_dump(exclude_none=True).items():
        setattr(control_type, key, value)
    session.commit()
    session.refresh(control_type)
    return control_type


@router.delete(
    '/{control_type_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Control type successfully deleted'},
        404: {'description': 'Control type not found'},
    },
    summary='Delete the control type'
)
def delete_control_type(control_type_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Response:
    """Delete the control type with the specified id."""
    control_type = session.get(ControlType, control_type_id)
    if not control_type:
        raise ControlTypeNotFoundException()
    session.delete(control_type)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '',
    responses={200: {'description': 'Control types successfully received'}},
    summary='Return a list of control types'
)
def get_control_types(session: SessionDep) -> list[ControlTypeRead]:
    """Return a list of control types."""
    control_types = session.execute(select(ControlType)).scalars()
    return control_types


@router.post(
    '',
    response_model=ControlTypeRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Control type successfully created'},
        409: {'description': 'Control type data is not unique'}
    },
    summary='Create the control type'
)
def create_control_type(control_type_data: ControlTypeCreate, session: SessionDep) -> Any:
    """Create the control type with the given information."""
    stmt = select(exists().where(ControlType.name == control_type_data.name))
    if session.execute(stmt).scalar():
        raise ControlTypeNameIsNotUniqueException()

    control_type = ControlType(**control_type_data.model_dump())
    session.add(control_type)
    session.commit()
    session.refresh(control_type)
    return control_type
