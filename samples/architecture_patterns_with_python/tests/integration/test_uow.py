from datetime import date
from typing import Optional

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from samples.architecture_patterns_with_python.allocation.domain.model import OrderLine
from samples.architecture_patterns_with_python.allocation.services.unit_of_work import (
    SQLAlchemyUnitOfWork,
)


def insert_batch(
    session: Session, ref: str, sku: str, qty: int, eta: Optional[date]
) -> None:
    session.execute(
        text(
            "INSERT INTO batch (reference, sku, _purchased_qty, eta)"
            " VALUES (:ref, :sku, :qty, :eta)"
        ),
        dict(ref=ref, sku=sku, qty=qty, eta=eta),
    )


def get_allocated_batch_ref(session: Session, order_id: str, sku: str) -> str:
    [[order_line_id]] = session.execute(
        text("SELECT id FROM order_line WHERE order_id=:order_id AND sku=:sku"),
        dict(order_id=order_id, sku=sku),
    )
    [[batch_ref]] = session.execute(
        text(
            "SELECT b.reference FROM allocation JOIN batch AS b ON batch_id = b.id"
            " WHERE order_line_id=:order_line_id"
        ),
        dict(order_line_id=order_line_id),
    )
    return batch_ref


def test_uow_can_retrieve_a_batch_and_allocate_to_it(
    session_factory: sessionmaker,
) -> None:
    session = session_factory()
    insert_batch(session, 'batch1', 'HIPSTER-WORKBENCH', 100, None)
    session.commit()

    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        batch = uow.batches.get(reference='batch1')
        line = OrderLine('o1', 'HIPSTER-WORKBENCH', 10)
        batch.allocate(line)
        uow.commit()

    batch_ref = get_allocated_batch_ref(session, 'o1', 'HIPSTER-WORKBENCH')
    assert batch_ref == 'batch1'


def test_rolls_back_uncommitted_work_by_default(session_factory: sessionmaker) -> None:
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        insert_batch(uow.session, 'batch1', 'MEDIUM-PLINTH', 100, None)

    new_session = session_factory()
    rows = list(new_session.execute(text('SELECT * FROM "batch"')))
    assert rows == []


def test_rolls_back_on_error(session_factory: sessionmaker) -> None:
    class MyException(Exception):
        pass

    uow = SQLAlchemyUnitOfWork(session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_batch(uow.session, 'batch1', 'LARGE-FORK', 100, None)
            raise MyException()

    new_session = session_factory()
    rows = list(new_session.execute(text('SELECT * FROM "batch"')))
    assert rows == []
