from sqlalchemy.orm import Session
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import Competency


class CompetenciesRepository(SQLAlchemyRepository):
    def __init__(self, session: Session):
        super().__init__(session, Competency)
