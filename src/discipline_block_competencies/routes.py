from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from sqlalchemy import select
from typing import Annotated, Any
from src.dependencies import SessionDep
from src.exceptions import (
    DisciplineBlockCompetencyNotFoundException, DisciplineBlockNotFoundException, CompetencyNotFoundException
)
from src.competencies.model import Competency
from .model import DisciplineBlockCompetency
from src.discipline_blocks.model import DisciplineBlock
from .schemas import DisciplineBlockCompetencyCreate, DisciplineBlockCompetencyUpdate, DisciplineBlockCompetencyRead

router = APIRouter(
    prefix='/discipline-block-competencies',
    tags=['discipline block competencies']
)


@router.get(
    '/{discipline_block_competency_id}',
    responses={
        200: {'description': 'Discipline block competency successfully received'},
        404: {'description': 'Discipline block competency not found'}
    },
    summary='Return the discipline block competency'
)
def get_discipline_block_competency(
        discipline_block_competency_id: Annotated[int, Path(gt=0)], session: SessionDep
) -> DisciplineBlockCompetencyRead:
    """Return the discipline block competency with the specified id"""
    discipline_block_competency = session.get(DisciplineBlockCompetency, discipline_block_competency_id)
    if not discipline_block_competency:
        raise DisciplineBlockCompetencyNotFoundException()
    return discipline_block_competency


@router.patch(
    '/{discipline_block_competency_id}',
    responses={
        200: {'description': 'Discipline block competency successfully updated'},
        404: {'description': 'Discipline block competency, discipline block or competency not found'}
    },
    summary='Update the discipline block competency'
)
def update_discipline_block_competency(
        discipline_block_competency_id: Annotated[int, Path(gt=0)],
        discipline_block_competency_data: DisciplineBlockCompetencyUpdate,
        session: SessionDep
) -> DisciplineBlockCompetencyRead:
    """
    Update the discipline block competency with the specified id with the given information
    (blank values are ignored)
    """
    discipline_block_competency = session.get(DisciplineBlockCompetency, discipline_block_competency_id)
    if not discipline_block_competency:
        raise DisciplineBlockCompetencyNotFoundException()

    if discipline_block_competency.discipline_block_id:
        if not session.get(DisciplineBlock, discipline_block_competency_data.discipline_block_id):
            raise DisciplineBlockNotFoundException()

    if discipline_block_competency.competency_id:
        if not session.get(Competency, discipline_block_competency_data.competency_id):
            raise CompetencyNotFoundException()

    for key, value in discipline_block_competency_data.model_dump(exclude_none=True).items():
        setattr(discipline_block_competency, key, value)
    session.commit()
    session.refresh(discipline_block_competency)
    return discipline_block_competency


@router.delete(
    '/{discipline_block_competency_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Discipline block competency successfully deleted'},
        404: {'description': 'Discipline block competency not found'},
    },
    summary='Delete the discipline block competency'
)
def delete_discipline_block_competency(
        discipline_block_competency_id: Annotated[int, Path(gt=0)], session: SessionDep
) -> Response:
    """Delete the discipline block competency with the specified id."""
    discipline_block_competency = session.get(DisciplineBlockCompetency, discipline_block_competency_id)
    if not discipline_block_competency:
        raise DisciplineBlockCompetencyNotFoundException()
    session.delete(discipline_block_competency)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '',
    responses={200: {'description': 'Discipline block competencies successfully received'}},
    summary='Return a list of discipline block competencies'
)
def get_discipline_block_competencies(session: SessionDep) -> list[DisciplineBlockCompetencyRead]:
    """Return a list of discipline block competencies."""
    discipline_block_competencies = session.execute(select(DisciplineBlockCompetency)).scalars()
    return discipline_block_competencies


@router.post(
    '',
    response_model=DisciplineBlockCompetencyRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Discipline block competency successfully created'},
        404: {'description': 'Discipline block or competency not found'}
    },
    summary='Create the discipline block competency'
)
def create_discipline_block_competency(
        discipline_block_competency_data: DisciplineBlockCompetencyCreate, session: SessionDep
) -> Any:
    """Create the discipline block competency with the given information."""
    if not session.get(DisciplineBlock, discipline_block_competency_data.discipline_block_id):
        raise DisciplineBlockNotFoundException()

    if not session.get(Competency, discipline_block_competency_data.competency_id):
        raise CompetencyNotFoundException()

    discipline_block_competency = DisciplineBlockCompetency(**discipline_block_competency_data.model_dump())
    session.add(discipline_block_competency)
    session.commit()
    session.refresh(discipline_block_competency)
    return discipline_block_competency
