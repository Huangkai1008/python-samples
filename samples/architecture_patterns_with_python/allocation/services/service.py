from datetime import date
from typing import Optional

from samples.architecture_patterns_with_python.allocation.domain import model
from samples.architecture_patterns_with_python.allocation.domain.model import (
    OrderLine,
    Product,
)
from samples.architecture_patterns_with_python.allocation.services.unit_of_work import (
    AbstractUnitOfWork,
)


class InvalidSKU(Exception):
    ...


def add_batch(
    ref: str,
    sku: str,
    qty: int,
    eta: Optional[date],
    uow: AbstractUnitOfWork,
) -> None:
    with uow:
        product = uow.products.get(sku)
        if product is None:
            product = Product(sku, batches=[])
            uow.products.add(product)

        product.batches.append(model.Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(
    order_id: str,
    sku: str,
    qty: int,
    uow: AbstractUnitOfWork,
) -> str:
    line = OrderLine(order_id, sku, qty)
    with uow:
        product = uow.products.get(line.sku)
        if not product:
            raise InvalidSKU(f'Invalid sku {line.sku}')
        batch_ref = product.allocate(line)
        uow.commit()
    return batch_ref
