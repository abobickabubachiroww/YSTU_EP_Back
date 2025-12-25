from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from typing import TypeVar, Generic
from .abstract_repository import AbstractRepository

T = TypeVar('T')


class SQLAlchemyRepository(AbstractRepository, Generic[T]):
    def __init__(self, session: Session, model: T):
        self.session: Session = session
        self.model: T = model

    def get_all(self) -> list[T]:
        stmt = select(self.model)
        res = self.session.execute(stmt)
        return list(res.scalars())

    def get_by_id(self, _id: int) -> T | None:
        res = self.session.get(self.model, _id)
        return res

    def create(self, data: dict) -> T:
        instance = self.model(**data)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def update(self, _id: int, data: dict) -> T | None:
        instance = self.get_by_id(_id)
        if not instance:
            return None

        for key, value in data.items():
            setattr(instance, key, value)

        self.session.commit()
        self.session.refresh(instance)
        return instance

    def delete(self, _id: int) -> bool:
        instance = self.get_by_id(_id)
        if not instance:
            return False

        self.session.delete(instance)
        self.session.commit()
        return True

    def filter_by(self, **filters) -> list[T]:
        stmt = select(self.model).filter_by(**filters)
        res = self.session.execute(stmt)
        return list(res.scalars())

    def exists(self, **filters) -> bool:
        conditions = [getattr(self.model, key) == value for key, value in filters.items()]
        stmt = select(exists().where(and_(*conditions)))
        res = self.session.execute(stmt)
        return res.scalar()
