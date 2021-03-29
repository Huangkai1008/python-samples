from typing import Generator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from samples.architecture_patterns_with_python.orm import mapper_registry, start_mappers


@pytest.fixture
def in_memory_db() -> Engine:
    engine = create_engine('sqlite:///:memory:')
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db: Engine) -> Generator[Session, None, None]:
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
