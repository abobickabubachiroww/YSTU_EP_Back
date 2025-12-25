from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from sqlalchemy import select
from typing import Annotated, Any
from src.dependencies import SessionDep
from src.exceptions import MapCoreNotFoundException
from .model import MapCore
from .schemas import MapCoreCreate, MapCoreUpdate, MapCoreRead

router = APIRouter(
    prefix='/map-cors',
    tags=['map cors']
)


@router.get(
    '/{map_core_id}',
    responses={
        200: {'description': 'Map core  successfully received'},
        404: {'description': 'Map core not found'}
    },
    summary='Return the map core'
)
def get_map_core(map_core_id: Annotated[int, Path(gt=0)], session: SessionDep) -> MapCoreRead:
    """Return the map core with the specified id"""
    map_core = session.get(MapCore, map_core_id)
    if not map_core:
        raise MapCoreNotFoundException()
    return map_core


@router.patch(
    '/{map_core_id}',
    responses={
        200: {'description': 'Map core successfully updated'},
        404: {'description': 'Map core not found'}
    },
    summary='Update the map core'
)
def update_map_core(
        map_core_id: Annotated[int, Path(gt=0)], map_core_data: MapCoreUpdate,
        session: SessionDep
) -> MapCoreRead:
    """Update the map core with the specified id with the given information (blank values are ignored)"""
    map_core = session.get(MapCore, map_core_id)
    if not map_core:
        raise MapCoreNotFoundException()

    for key, value in map_core_data.model_dump(exclude_none=True).items():
        setattr(map_core, key, value)
    session.commit()
    session.refresh(map_core)
    return map_core


@router.delete(
    '/{map_core_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Map core successfully deleted'},
        404: {'description': 'Map core not found'},
    },
    summary='Delete the map core'
)
def delete_map_core(map_core_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Response:
    """Delete the map core group with the specified id."""
    map_core = session.get(MapCore, map_core_id)
    if not map_core:
        raise MapCoreNotFoundException()
    session.delete(map_core)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '',
    responses={200: {'description': 'Map cores successfully received'}},
    summary='Return a list of map cores'
)
def get_map_cores(session: SessionDep) -> list[MapCoreRead]:
    """Return a list of map cors."""
    map_cores = session.execute(select(MapCore)).scalars()
    return map_cores


@router.post(
    '',
    response_model=MapCoreRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Map core successfully created'}
    },
    summary='Create the map core'
)
def create_map_core(map_core_data: MapCoreCreate, session: SessionDep) -> Any:
    """Create the map core with the given information."""
    map_core = MapCore(**map_core_data.model_dump())
    session.add(map_core)
    session.commit()
    session.refresh(map_core)
    return map_core
