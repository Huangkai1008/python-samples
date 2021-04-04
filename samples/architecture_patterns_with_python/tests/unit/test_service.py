from typing import Iterable, List, Optional, Set

import pytest

from samples.architecture_patterns_with_python.allocation.adapter.repository import (
    AbstractRepository,
)
from samples.architecture_patterns_with_python.allocation.domain.model import Batch
from samples.architecture_patterns_with_python.allocation.services import service
from samples.architecture_patterns_with_python.allocation.services.service import (
    InvalidSKU,
    allocate,
)
from samples.architecture_patterns_with_python.allocation.services.unit_of_work import (
    AbstractUnitOfWork,
)


class FakeRepository(AbstractRepository):
    def __init__(self, batches: Iterable[Batch]) -> None:
        self._batches: Set[Batch] = set(batches)

    def add(self, batch: Batch) -> None:
        self._batches.add(batch)

    def get(self, reference: str) -> Optional[Batch]:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> List[Batch]:
        return list(self._batches)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.batches = FakeRepository([])
        self.committed: bool = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass


class FakeSession:
    committed: bool = False

    def commit(self) -> None:
        self.committed = True


def test_add_batch() -> None:
    uow = FakeUnitOfWork()

    service.add_batch('b1', 'COMPLICATED-LAMP', 100, None, uow)

    assert uow.batches.get('b1') is not None
    assert uow.committed


def test_allocate_returns_allocation() -> None:
    uow = FakeUnitOfWork()

    service.add_batch('b1', 'COMPLICATED-LAMP', 100, None, uow)
    result = service.allocate('o1', 'COMPLICATED-LAMP', 10, uow)

    assert result == 'b1'


def test_allocate_errors_for_invalid_sku() -> None:
    uow = FakeUnitOfWork()

    service.add_batch('b1', 'AREAL_SKU', 100, None, uow)

    with pytest.raises(InvalidSKU, match='Invalid sku NON_EXISTENT_SKU'):
        allocate('o1', 'NON_EXISTENT_SKU', 10, uow)


def test_allocate_commits() -> None:
    uow = FakeUnitOfWork()

    service.add_batch('b1', 'OMINOUS-MIRROR', 100, None, uow)
    service.allocate('o1', 'OMINOUS-MIRROR', 10, uow)

    assert uow.committed
