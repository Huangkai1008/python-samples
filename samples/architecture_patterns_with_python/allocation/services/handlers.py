from samples.architecture_patterns_with_python.allocation.adapter import email
from samples.architecture_patterns_with_python.allocation.domain import model
from samples.architecture_patterns_with_python.allocation.domain.command import (
    Allocate,
    ChangeBatchQuantity,
    CreateBatch,
)
from samples.architecture_patterns_with_python.allocation.domain.event import OutOfStock
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
    cmd: CreateBatch,
    uow: AbstractUnitOfWork,
) -> None:
    with uow:
        product = uow.products.get(cmd.sku)
        if product is None:
            product = Product(cmd.sku, batches=[])
            uow.products.add(product)

        product.batches.append(model.Batch(cmd.ref, cmd.sku, cmd.qty, cmd.eta))
        uow.commit()


def allocate(
    cmd: Allocate,
    uow: AbstractUnitOfWork,
) -> str:
    line = OrderLine(cmd.order_id, cmd.sku, cmd.qty)
    with uow:
        product = uow.products.get(line.sku)
        if not product:
            raise InvalidSKU(f'Invalid sku {line.sku}')
        batch_ref = product.allocate(line)
        uow.commit()
    return batch_ref


def change_batch_quantity(
    cmd: ChangeBatchQuantity,
    uow: AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get_by_batch_ref(cmd.ref)
        product.change_batch_quantity(cmd.ref, cmd.qty)


def send_out_of_stock_notification(
    event: OutOfStock,
):
    email.send_mail(
        'stock@made.com',
        f'Out of stock for {event.sku}',
    )
