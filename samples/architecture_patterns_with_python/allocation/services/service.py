from typing import Iterable

from samples.architecture_patterns_with_python.allocation.domain import model
from samples.architecture_patterns_with_python.allocation.domain.model import Batch, OrderLine
from samples.architecture_patterns_with_python.allocation.adapter.repository import (
    AbstractRepository,
    AbstractSession,
)


class InvalidSKU(Exception):
    ...


def is_valid_sku(sku: str, batches: Iterable[Batch]) -> bool:
    return sku in {b.sku for b in batches}


def allocate(
    line: OrderLine, repo: AbstractRepository, session: AbstractSession
) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSKU(f'Invalid sku {line.sku}')

    batch_ref = model.allocate(line, batches)
    session.commit()
    return batch_ref
