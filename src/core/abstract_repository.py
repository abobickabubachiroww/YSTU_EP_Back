from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, _id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    def update(self, _id: int, data: dict) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, _id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def filter_by(self, **filters) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def exists(self, **filters) -> bool:
        raise NotImplementedError
