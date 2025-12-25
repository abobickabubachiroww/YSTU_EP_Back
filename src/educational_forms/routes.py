from fastapi import APIRouter, status, Path
from fastapi.responses import Response
from sqlalchemy import select, exists, and_
from typing import Annotated, Any
from src.dependencies import SessionDep
from src.exceptions import EducationalFormNotFoundException, EducationalFormNameIsNotUniqueException
from .model import EducationalForm
from .schemas import EducationalFormCreate, EducationalFormUpdate, EducationalFormRead

router = APIRouter(
    prefix='/educational-forms',
    tags=['educational forms']
)


@router.get(
    '/{educational_form_id}',
    responses={
        200: {'description': 'Educational form successfully received'},
        404: {'description': 'Educational form not found'}
    },
    summary='Return the educational form'
)
def get_educational_form(
        educational_form_id: Annotated[int, Path(gt=0)], session: SessionDep
) -> EducationalFormRead:
    """Return the educational form with the specified id"""
    educational_form = session.get(EducationalForm, educational_form_id)
    if not educational_form:
        raise EducationalFormNotFoundException()
    return educational_form


@router.patch(
    '/{educational_form_id}',
    responses={
        200: {'description': 'Educational form successfully updated'},
        404: {'description': 'Educational form not found'},
        409: {'description': 'Educational form data is not unique'}
    },
    summary='Update the educational form'
)
def update_educational_form(
        educational_form_id: Annotated[int, Path(gt=0)],
        educational_form_data: EducationalFormUpdate,
        session: SessionDep
) -> EducationalFormRead:
    """Update the educational form with the specified id with the given information (blank values are ignored)"""
    educational_form = session.get(EducationalForm, educational_form_id)
    if not educational_form:
        raise EducationalFormNotFoundException()

    if educational_form_data.name:
        stmt = select(exists().where(and_(
            EducationalForm.name == educational_form_data.name, EducationalForm.id != educational_form_id
        )))
        if session.execute(stmt).scalar():
            raise EducationalFormNameIsNotUniqueException()

    for key, value in educational_form_data.model_dump(exclude_none=True).items():
        setattr(educational_form, key, value)
    session.commit()
    session.refresh(educational_form)
    return educational_form


@router.delete(
    '/{educational_form_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'description': 'Educational form successfully deleted'},
        404: {'description': 'Educational form not found'},
    },
    summary='Delete the educational form'
)
def delete_educational_form(educational_form_id: Annotated[int, Path(gt=0)], session: SessionDep) -> Response:
    """Delete the educational form with the specified id."""
    educational_form = session.get(EducationalForm, educational_form_id)
    if not educational_form:
        raise EducationalFormNotFoundException()
    session.delete(educational_form)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '',
    responses={200: {'description': 'Educational forms successfully received'}},
    summary='Return a list of educational forms'
)
def get_educational_forms(session: SessionDep) -> list[EducationalFormRead]:
    """Return a list of educational forms."""
    educational_forms = session.execute(select(EducationalForm)).scalars()
    return educational_forms


@router.post(
    '',
    response_model=EducationalFormRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {'description': 'Educational form successfully created'},
        409: {'description': 'Educational form data is not unique'}
    },
    summary='Create the educational form'
)
def create_educational_form(educational_form_data: EducationalFormCreate, session: SessionDep) -> Any:
    """Create the educational form with the given information."""
    stmt = select(exists().where(EducationalForm.name == educational_form_data.name))
    if session.execute(stmt).scalar():
        raise EducationalFormNameIsNotUniqueException()

    educational_form = EducationalForm(**educational_form_data.model_dump())
    session.add(educational_form)
    session.commit()
    session.refresh(educational_form)
    return educational_form
