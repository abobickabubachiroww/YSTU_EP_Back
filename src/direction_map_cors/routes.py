from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from sqlalchemy import select
from typing import Annotated, Any
from src.dependencies import SessionDep
from src.exceptions import DirectionMapCoreNotFoundException, DirectionNotFoundException, MapCoreNotFoundException
from .model import DirectionMapCore
from src.map_cors.model import MapCore
from src.directions.model import Direction
from .schemas import DirectionMapCoreCreate, DirectionMapCoreUpdate, DirectionMapCoreRead

router = APIRouter(
    prefix='/direction-map-cors',
    tags=['direction map cors']
)


@router.get(
    '/{direction_map_core_id}',
    responses={
        200: {'description': 'Direction map core successfully received'},
        404: {'description': 'Direction map core not found'}
    },
    summary='Return the direction map core'
)
def get_direction_map_core(
        direction_map_core_id: Annotated[int, Path(gt=0)], session: SessionDep
) -> DirectionMapCoreRead:
    """Return the direction map core with the specified id"""
    direction_map_core = session.get(DirectionMapCore, direction_map_core_id)
    if not direction_map_core:
        raise DirectionMapCoreNotFoundException()
    return direction_map_core


@router.patch(
    '/{direction_map_core_id}',
    responses={
        200: {'description': 'Direction map core successfully updated'},
        404: {'description': 'Direction map core, direction or map core not found'}
    },
    summary='Update the direction map core'
)
def update_direction_map_core(
        direction_map_core_id: Annotated[int, Path(gt=0)],
        direction_map_core_data: DirectionMapCoreUpdate,
        session: SessionDep
) -> DirectionMapCoreRead:
    """
    Update the direction map core with the specified id with the given information
    (blank values are ignored)
    """
    direction_map_core = session.get(DirectionMapCore, direction_map_core_id)
    if not direction_map_core:
        raise DirectionMapCoreNotFoundException()

    if direction_map_core.direction_id:
        if not session.get(Direction, direction_map_core_data.direction_id):
            raise DirectionNotFoundException()

    if direction_map_core.map_core_id:
        if not session.get(MapCore, direction_map_core_data.map_core_id):
            raise MapCoreNotFoundException()

    for key, value in direction_map_core_data.model_dump(exclude_none=True).items():
        setattr(direction_map_core, key, value)
    session.commit()
    session.refresh(direction_map_core)
    return direction_map_core


@router.delete(
    '/{direction_map_core_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Direction map core successfully deleted'},
        404: {'description': 'Direction map core not found'},
    },
    summary='Delete the direction map core'
)
def delete_direction_map_core(
        direction_map_core_id: Annotated[int, Path(gt=0)], session: SessionDep
) -> Response:
    """Delete the direction map core with the specified id."""
    direction_map_core = session.get(DirectionMapCore, direction_map_core_id)
    if not direction_map_core:
        raise DirectionMapCoreNotFoundException()
    session.delete(direction_map_core)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '',
    responses={200: {'description': 'Direction map cors successfully received'}},
    summary='Return a list of direction map cors'
)
def get_direction_map_cors(session: SessionDep) -> list[DirectionMapCoreRead]:
    """Return a list of direction map cors."""
    direction_map_cors = session.execute(select(DirectionMapCore)).scalars()
    return direction_map_cors


@router.post(
    '',
    response_model=DirectionMapCoreRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Direction map core successfully created'},
        404: {'description': 'Direction or map core not found'}
    },
    summary='Create the direction map core'
)
def create_direction_map_core(
        direction_map_core_data: DirectionMapCoreCreate, session: SessionDep
) -> Any:
    """Create the direction map core with the given information."""
    if not session.get(Direction, direction_map_core_data.direction_id):
        raise DirectionNotFoundException()

    if not session.get(MapCore, direction_map_core_data.map_core_id):
        raise MapCoreNotFoundException()

    direction_map_core = DirectionMapCore(**direction_map_core_data.model_dump())
    session.add(direction_map_core)
    session.commit()
    session.refresh(direction_map_core)
    return direction_map_core
