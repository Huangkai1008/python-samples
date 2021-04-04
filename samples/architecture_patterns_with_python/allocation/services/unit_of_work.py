from abc import ABC, abstractmethod
from traceback import TracebackException
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing_extensions import Self

from samples.architecture_patterns_with_python import config
from samples.architecture_patterns_with_python.allocation.adapter.repository import (
    AbstractRepository,
    SQLAlchemyRepository,
)


class AbstractUnitOfWork(ABC):
    products: AbstractRepository

    @abstractmethod
    def commit(self) -> None:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: TracebackException,
    ) -> None:
        self.rollback()


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_database_uri(),
    ),
    isolation_level='REPEATABLE READ',
)


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: sessionmaker = DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory: sessionmaker = session_factory

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        self.batches = SQLAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: TracebackException,
    ) -> None:
        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.close()
