from sqlalchemy.orm import Session
from src.core.sqlalchemy_repository import SQLAlchemyRepository
from .model import ActivityType


class ActivityTypesRepository(SQLAlchemyRepository):
    def __init__(self, session: Session):
        super().__init__(session, ActivityType)
