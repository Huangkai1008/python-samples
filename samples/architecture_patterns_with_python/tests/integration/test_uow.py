import threading
import time
import traceback
from datetime import date
from typing import List, Optional

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from samples.architecture_patterns_with_python.allocation.domain.model import OrderLine
from samples.architecture_patterns_with_python.allocation.services.unit_of_work import (
    SQLAlchemyUnitOfWork,
)
from samples.architecture_patterns_with_python.tests.random_refs import (
    random_batch_ref,
    random_order_id,
    random_sku,
)


def insert_batch(
    session: Session,
    ref: str,
    sku: str,
    qty: int,
    eta: Optional[date],
    product_version: int = 1,
) -> None:
    session.execute(
        text("INSERT INTO product (sku, version_number) VALUES (:sku, :version)"),
        dict(sku=sku, version=product_version),
    )
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
        product = uow.products.get('HIPSTER-WORKBENCH')
        line = OrderLine('o1', 'HIPSTER-WORKBENCH', 10)
        product.allocate(line)
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


def try_to_allocate(order_id: str, sku: str, exceptions: List[Exception]) -> None:
    line = OrderLine(order_id, sku, 10)
    try:
        with SQLAlchemyUnitOfWork() as uow:
            product = uow.products.get(sku)
            product.allocate(line)
            time.sleep(0.2)
            uow.commit()
    except Exception as e:
        print(traceback.format_exc())
        exceptions.append(e)


@pytest.mark.skip('Use MySQL instead')
def test_concurrent_updates_to_version_are_not_allowed(
    session_factory: sessionmaker,
) -> None:
    sku, batch = random_sku(), random_batch_ref()
    session = session_factory()
    insert_batch(session, batch, sku, 100, eta=None, product_version=1)
    session.commit()

    order1, order2 = random_order_id('1'), random_order_id('2')
    exceptions = []
    t1 = threading.Thread(target=lambda: try_to_allocate(order1, sku, exceptions))
    t2 = threading.Thread(target=lambda: try_to_allocate(order2, sku, exceptions))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    [[version]] = session.execute(
        text("SELECT version_number FROM product WHERE sku=:sku"),
        dict(sku=sku),
    )
    assert version == 2
    [exception] = exceptions
    assert 'could not serialize access due to concurrent update' in str(exception)

    orders = session.execute(
        text(
            "SELECT order_id FROM allocation"
            " JOIN batch ON allocation.batch_id = batches.id"
            " JOIN order_line ON allocation.order_line_id = order_line.id"
            " WHERE order_line.sku=:sku"
        ),
        dict(sku=sku),
    )
    assert orders.rowcount == 1
    with SQLAlchemyUnitOfWork() as uow:
        uow.session.execute(text('select 1'))
