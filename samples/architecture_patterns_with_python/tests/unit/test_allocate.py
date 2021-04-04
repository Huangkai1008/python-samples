from datetime import date, timedelta

import pytest

from samples.architecture_patterns_with_python.allocation.domain.model import (
    Batch,
    OrderLine,
    OutOfStock,
    allocate,
)

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments() -> None:
    in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100)
    shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, eta=tomorrow)
    line = OrderLine('order-ref', 'RETRO-CLOCK', 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_qty == 90
    assert shipment_batch.available_qty == 100


def test_prefers_earlier_batches() -> None:
    earliest = Batch('speedy-batch', 'MINIMALIST-SPOON', 100, eta=today)
    medium = Batch('normal-batch', 'MINIMALIST-SPOON', 100, eta=tomorrow)
    latest = Batch('slow-batch', 'MINIMALIST-SPOON', 100, eta=later)
    line = OrderLine('order1', 'MINIMALIST-SPOON', 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.available_qty == 90
    assert medium.available_qty == 100
    assert latest.available_qty == 100


def test_returns_allocated_batch_ref() -> None:
    in_stock_batch = Batch('in-stock-batch-ref', 'HIGHBROW-POSTER', 100, eta=None)
    shipment_batch = Batch('shipment-batch-ref', 'HIGHBROW-POSTER', 100, eta=tomorrow)
    line = OrderLine('order-ref', 'HIGHBROW-POSTER', 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate() -> None:
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])

    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])
