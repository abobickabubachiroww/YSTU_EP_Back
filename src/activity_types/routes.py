from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from sqlalchemy import select, exists, and_
from typing import Annotated, Any
from src.dependencies import SessionDep
from src.exceptions import ActivityTypeNotFoundException, ActivityTypeNameIsNotUniqueException
from .model import ActivityType
from .schemas import ActivityTypeCreate, ActivityTypeUpdate, ActivityTypeRead

router = APIRouter(
    prefix='/activity-types',
    tags=['activity types']
)


@router.get(
    '/{activity_type_id}',
    responses={
        200: {'description': 'Activity type successfully received'},
        404: {'description': 'Activity type not found'}
    },
    summary='Return the activity type'
)
def get_activity_type(activity_type_id: Annotated[int, Path(gt=0)], session: SessionDep) -> ActivityTypeRead:
    """Return the activity type with the specified id"""
    activity_type = session.get(ActivityType, activity_type_id)
    if not activity_type:
        raise ActivityTypeNotFoundException()
    return activity_type


@router.patch(
    '/{activity_type_id}',
    responses={
        200: {'description': 'Activity type successfully updated'},
        404: {'description': 'Activity type not found'},
        409: {'description': 'Activity type data is not unique'}
    },
    summary='Update the activity type'
)
def update_activity_type(
        activity_type_id: Annotated[int, Path(gt=0)], activity_type_data: ActivityTypeUpdate, session: SessionDep
) -> ActivityTypeRead:
    """Update the activity type with the specified id with the given information (blank values are ignored)"""
    activity_type = session.get(ActivityType, activity_type_id)
    if not activity_type:
        raise ActivityTypeNotFoundException()

    if activity_type_data.name:
        stmt = select(exists().where(and_(
            ActivityType.name == activity_type_data.name, ActivityType.id != activity_type_id
        )))
        if session.execute(stmt).scalar():
            raise ActivityTypeNameIsNotUniqueException()

    for key, value in activity_type_data.model_dump(exclude_none=True).items():
        setattr(activity_type, key, value)
    session.commit()
    session.refresh(activity_type)
    return activity_type


@router.delete(
    '/{activity_type_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Activity type successfully deleted'},
        404: {'description': 'Activity type not found'},
    },
    summary='Delete the activity type'
)
def delete_activity_type(activity_type_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Response:
    """Delete the activity type with the specified id."""
    activity_type = session.get(ActivityType, activity_type_id)
    if not activity_type:
        raise ActivityTypeNotFoundException()
    session.delete(activity_type)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '',
    responses={200: {'description': 'Activity types successfully received'}},
    summary='Return a list of activity types'
)
def get_activity_types(session: SessionDep) -> list[ActivityTypeRead]:
    """Return a list of activity types."""
    activity_types = session.execute(select(ActivityType)).scalars()
    return activity_types


@router.post(
    '',
    response_model=ActivityTypeRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Activity type successfully created'},
        409: {'description': 'Activity type data is not unique'}
    },
    summary='Create the activity type'
)
def create_activity_type(activity_type_data: ActivityTypeCreate, session: SessionDep) -> Any:
    """Create the activity type with the given information."""
    stmt = select(exists().where(ActivityType.name == activity_type_data.name))
    if session.execute(stmt).scalar():
        raise ActivityTypeNameIsNotUniqueException()

    activity_type = ActivityType(**activity_type_data.model_dump())
    session.add(activity_type)
    session.commit()
    session.refresh(activity_type)
    return activity_type
