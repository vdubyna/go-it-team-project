from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
from .base_entity import BaseEntity

T = TypeVar('T', bound=BaseEntity)

class BaseCollection(ABC, Generic[T]):
    def search(self, query: str, tag: str = "", sort: str = "name", order: str = "asc") -> List[T]:
        """Get the entities sorted by the passed parameters."""
        result: List[T] = []
        for entity in self.get_all():
            matched = self._match_entity(entity, query.lower(), tag)
            if matched: 
                result.append(matched)
        return sorted(
            result,
            key=lambda entity: getattr(entity, sort).value,
            reverse=(order != "asc"),
        )

    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities. Must be implemented by the child class."""
        pass

    @abstractmethod
    def _match_entity(self, entity: T, query: str, tag: str = "") -> bool:
        """Check if the entity matches the query. Must be implemented by the child class."""
        pass
