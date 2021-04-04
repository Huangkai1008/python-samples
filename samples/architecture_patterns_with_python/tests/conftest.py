import time
from pathlib import Path
from typing import Generator, Optional

import pytest
import requests
from requests import Response
from sqlalchemy import Connection, Engine, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from samples.architecture_patterns_with_python import config
from samples.architecture_patterns_with_python.allocation.adapter.orm import (
    mapper_registry,
    start_mappers,
)


@pytest.fixture
def in_memory_db() -> Engine:
    engine = create_engine('sqlite:///:memory:')
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db: Engine) -> Generator[sessionmaker, None, None]:
    start_mappers()
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def session(session_factory: sessionmaker) -> Session:
    return session_factory()


def wait_for_database_to_come_up(engine: Engine) -> Optional[Connection]:
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail('Database never came up')


def wait_for_webapp_to_come_up() -> Response:
    deadline = time.time() + 10
    url = config.get_api_url()
    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail('API never came up')


@pytest.fixture(scope='session')
def database() -> Engine:
    engine = create_engine(config.get_database_uri())
    wait_for_database_to_come_up(engine)
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def database_session(database: Engine) -> Generator[Session, None, None]:
    start_mappers()
    yield sessionmaker(bind=database)()
    clear_mappers()


@pytest.fixture
def restart_api() -> None:
    (Path(__file__).parent.parent / 'autoapp.py').touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()
