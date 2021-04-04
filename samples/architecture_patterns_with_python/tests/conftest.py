import time
from pathlib import Path
from typing import Any, Generator, List, Optional

import pytest
import requests
from requests import Response
from sqlalchemy import Connection, Engine, create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from samples.architecture_patterns_with_python import config
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
def add_stock(database_session: Session) -> Any:
    batches_added = set()
    skus_added = set()

    def _add_stock(lines: List) -> None:
        for ref, sku, qty, eta in lines:
            database_session.execute(
                text(
                    "INSERT INTO batch (reference, sku, _purchased_qty, eta)"
                    " VALUES (:ref, :sku, :qty, :eta)"
                ),
                dict(ref=ref, sku=sku, qty=qty, eta=eta),
            )
            [[batch_id]] = database_session.execute(
                text("SELECT id FROM batch WHERE reference=:ref AND sku=:sku"),
                dict(ref=ref, sku=sku),
            )
            batches_added.add(batch_id)
            skus_added.add(sku)
        database_session.commit()

    yield _add_stock

    for batch_id in batches_added:
        database_session.execute(
            text("DELETE FROM allocation WHERE batch_id=:batch_id"),
            dict(batch_id=batch_id),
        )
        database_session.execute(
            text("DELETE FROM batch WHERE id=:batch_id"),
            dict(batch_id=batch_id),
        )
    for sku in skus_added:
        database_session.execute(
            text("DELETE FROM order_line WHERE sku=:sku"),
            dict(sku=sku),
        )
        database_session.commit()


@pytest.fixture
def restart_api() -> None:
    (Path(__file__).parent.parent / 'autoapp.py').touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()
