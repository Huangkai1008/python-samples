from datetime import date
from typing import Iterable, Optional

from samples.architecture_patterns_with_python.allocation.domain import model
from samples.architecture_patterns_with_python.allocation.domain.model import (
    Batch,
    OrderLine,
)
from samples.architecture_patterns_with_python.allocation.services.unit_of_work import (
    AbstractUnitOfWork,
)


class InvalidSKU(Exception):
    ...


def is_valid_sku(sku: str, batches: Iterable[Batch]) -> bool:
    return sku in {b.sku for b in batches}


def add_batch(
    ref: str,
    sku: str,
    qty: int,
    eta: Optional[date],
    uow: AbstractUnitOfWork,
) -> None:
    with uow:
        uow.batches.add(model.Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(
    order_id: str,
    sku: str,
    qty: int,
    uow: AbstractUnitOfWork,
) -> str:
    line = OrderLine(order_id, sku, qty)
    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(line.sku, batches):
            raise InvalidSKU(f'Invalid sku {line.sku}')
        batch_ref = model.allocate(line, batches)
        uow.commit()
    return batch_ref
