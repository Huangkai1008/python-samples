from datetime import date, timedelta

import pytest

from samples.architecture_patterns_with_python.allocation.domain.model import (
    Batch,
    OrderLine,
    OutOfStock,
    Product,
)

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments() -> None:
    in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100)
    shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, eta=tomorrow)
    product = Product('RETRO-CLOCK', [in_stock_batch, shipment_batch])
    line = OrderLine('order-ref', 'RETRO-CLOCK', 10)

    product.allocate(line)

    assert in_stock_batch.available_qty == 90
    assert shipment_batch.available_qty == 100


def test_prefers_earlier_batches() -> None:
    earliest = Batch('speedy-batch', 'MINIMALIST-SPOON', 100, eta=today)
    medium = Batch('normal-batch', 'MINIMALIST-SPOON', 100, eta=tomorrow)
    latest = Batch('slow-batch', 'MINIMALIST-SPOON', 100, eta=later)
    line = OrderLine('order1', 'MINIMALIST-SPOON', 10)
    product = Product('MINIMALIST-SPOON', [earliest, medium, latest])

    product.allocate(line)

    assert earliest.available_qty == 90
    assert medium.available_qty == 100
    assert latest.available_qty == 100


def test_returns_allocated_batch_ref() -> None:
    in_stock_batch = Batch('in-stock-batch-ref', 'HIGHBROW-POSTER', 100, eta=None)
    shipment_batch = Batch('shipment-batch-ref', 'HIGHBROW-POSTER', 100, eta=tomorrow)
    line = OrderLine('order-ref', 'HIGHBROW-POSTER', 10)
    product = Product('HIGHBROW-POSTER', [in_stock_batch, shipment_batch])

    allocation = product.allocate(line)

    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate() -> None:
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    product = Product('SMALL-FORK', [batch])
    line = OrderLine('order1', 'SMALL-FORK', 10)

    product.allocate(line)

    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        product.allocate(OrderLine('order2', 'SMALL-FORK', 1))


def test_increments_version_number() -> None:
    line = OrderLine('order1', 'SCANDI-PEN', 10)
    product = Product(
        'SCANDI-PEN', batches=[Batch('b1', 'SCANDI-PEN', 100)], version_number=7
    )

    product.allocate(line)

    assert product.version_number == 8
