from datetime import date
from typing import Tuple

from samples.architecture_patterns_with_python.allocation.domain.model import Batch, OrderLine


def make_batch_and_line(
    sku: str, batch_qty: int, line_qty: int
) -> Tuple[Batch, OrderLine]:
    return (
        Batch('batch-001', sku, batch_qty, eta=date.today()),
        OrderLine('order-ref', sku, line_qty),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity() -> None:
    batch, line = make_batch_and_line('SMALL-TABLE', 20, 2)

    batch.allocate(line)

    assert batch.available_qty == 18


def test_can_allocate_if_available_greater_than_required() -> None:
    batch, line = make_batch_and_line('ELEGANT-LAMP', 20, 2)

    assert batch.can_allocate(line)


def test_can_allocate_if_available_equal_required() -> None:
    batch, line = make_batch_and_line('ELEGANT-LAMP', 20, 20)

    assert batch.can_allocate(line)


def test_cannot_allocate_if_available_smaller_than_required() -> None:
    batch, line = make_batch_and_line('ELEGANT-LAMP', 2, 20)

    assert batch.can_allocate(line) is False


def test_cannot_allocate_if_skus_do_not_match() -> None:
    batch = Batch('batch-001', 'UNCOMFORTABLE-CHAIR', 100, eta=None)
    different_sku_line = OrderLine('order-123', 'EXPENSIVE-TOASTER', 10)

    assert batch.can_allocate(different_sku_line) is False


def test_allocation_is_idempotent() -> None:
    batch, line = make_batch_and_line('ANGULAR-DESK', 20, 2)

    batch.allocate(line)
    batch.allocate(line)

    assert batch.available_qty == 18


def test_can_only_deallocate_allocated_lines() -> None:
    batch, line = make_batch_and_line('DECORATIVE-TRINKET', 20, 2)

    batch.deallocate(line)

    assert batch.available_qty == 20
