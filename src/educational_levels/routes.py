from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from sqlalchemy import select, exists, and_
from typing import Annotated, Any
from src.dependencies import SessionDep
from src.exceptions import EducationalLevelNotFoundException, EducationalLevelNameIsNotUniqueException
from .model import EducationalLevel
from .schemas import EducationalLevelCreate, EducationalLevelUpdate, EducationalLevelRead

router = APIRouter(
    prefix='/educational-levels',
    tags=['educational levels']
)


@router.get(
    '/{educational_level_id}',
    responses={
        200: {'description': 'Educational level successfully received'},
        404: {'description': 'Educational level not found'}
    },
    summary='Return the educational level'
)
def get_educational_level(
        educational_level_id: Annotated[int, Path(gt=0)], session: SessionDep
) -> EducationalLevelRead:
    """Return the educational level with the specified id"""
    educational_level = session.get(EducationalLevel, educational_level_id)
    if not educational_level:
        raise EducationalLevelNotFoundException()
    return educational_level


@router.patch(
    '/{educational_level_id}',
    responses={
        200: {'description': 'Educational level successfully updated'},
        404: {'description': 'Educational level not found'},
        409: {'description': 'Educational level data is not unique'}
    },
    summary='Update the educational level'
)
def update_educational_level(
        educational_level_id: Annotated[int, Path(gt=0)],
        educational_level_data: EducationalLevelUpdate,
        session: SessionDep
) -> EducationalLevelRead:
    """Update the educational level with the specified id with the given information (blank values are ignored)"""
    educational_level = session.get(EducationalLevel, educational_level_id)
    if not educational_level:
        raise EducationalLevelNotFoundException()

    if educational_level_data.name:
        stmt = select(exists().where(and_(
            EducationalLevel.name == educational_level_data.name, EducationalLevel.id != educational_level_id
        )))
        if session.execute(stmt).scalar():
            raise EducationalLevelNameIsNotUniqueException()

    for key, value in educational_level_data.model_dump(exclude_none=True).items():
        setattr(educational_level, key, value)
    session.commit()
    session.refresh(educational_level)
    return educational_level


@router.delete(
    '/{educational_level_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Educational level successfully deleted'},
        404: {'description': 'Educational level not found'},
    },
    summary='Delete the educational level'
)
def delete_educational_level(educational_level_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Response:
    """Delete the educational level with the specified id."""
    educational_level = session.get(EducationalLevel, educational_level_id)
    if not educational_level:
        raise EducationalLevelNotFoundException()
    session.delete(educational_level)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '',
    responses={200: {'description': 'Educational levels successfully received'}},
    summary='Return a list of educational levels'
)
def get_educational_levels(session: SessionDep) -> list[EducationalLevelRead]:
    """Return a list of educational levels."""
    educational_levels = session.execute(select(EducationalLevel)).scalars()
    return educational_levels


@router.post(
    '',
    response_model=EducationalLevelRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Educational level successfully created'},
        409: {'description': 'Educational level data is not unique'}
    },
    summary='Create the educational level'
)
def create_educational_level(educational_level_data: EducationalLevelCreate, session: SessionDep) -> Any:
    """Create the educational level with the given information."""
    stmt = select(exists().where(EducationalLevel.name == educational_level_data.name))
    if session.execute(stmt).scalar():
        raise EducationalLevelNameIsNotUniqueException()

    educational_level = EducationalLevel(**educational_level_data.model_dump())
    session.add(educational_level)
    session.commit()
    session.refresh(educational_level)
    return educational_level
