from abc import ABCMeta, abstractmethod
from typing import List, Optional, Protocol

from sqlalchemy.orm import Session

from samples.architecture_patterns_with_python.model import Batch


class AbstractRepository(metaclass=ABCMeta):
    @abstractmethod
    def add(self, batch: Batch) -> None:
        ...

    @abstractmethod
    def get(self, reference: str) -> Optional[Batch]:
        ...

    @abstractmethod
    def list(self) -> List[Batch]:
        ...


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def add(self, batch: Batch) -> None:
        self.session.add(batch)

    def get(self, reference: str) -> Optional[Batch]:
        return self.session.query(Batch).filter_by(reference=reference).first()

    def list(self) -> List[Batch]:
        return self.session.query(Batch).all()


class AbstractSession(Protocol):
    def commit(self) -> None:
        ...
