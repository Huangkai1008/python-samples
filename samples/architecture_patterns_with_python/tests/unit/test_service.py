from typing import Iterable, List, Optional, Set

import pytest

from samples.architecture_patterns_with_python.allocation.domain.model import Batch, OrderLine
from samples.architecture_patterns_with_python.allocation.adapter.repository import AbstractRepository
from samples.architecture_patterns_with_python.allocation.services.service import InvalidSKU, allocate


class FakeRepository(AbstractRepository):
    def __init__(self, batches: Iterable[Batch]) -> None:
        self._batches: Set[Batch] = set(batches)

    def add(self, batch: Batch) -> None:
        self._batches.add(batch)

    def get(self, reference: str) -> Optional[Batch]:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> List[Batch]:
        return list(self._batches)


class FakeSession:
    committed: bool = False

    def commit(self) -> None:
        self.committed = True


def test_returns_allocation() -> None:
    line = OrderLine('o1', 'COMPLICATED-LAMP', 10)
    batch = Batch('b1', 'COMPLICATED-LAMP', 100, eta=None)
    repo = FakeRepository([batch])

    result = allocate(line, repo, FakeSession())

    assert result == 'b1'


def test_error_for_invalid_sku() -> None:
    line = OrderLine('o1', 'NON_EXISTENT_SKU', 10)
    batch = Batch('b1', 'AREAL_SKU', 100)
    repo = FakeRepository([batch])

    with pytest.raises(InvalidSKU, match='Invalid sku NON_EXISTENT_SKU'):
        allocate(line, repo, FakeSession())


def test_commits() -> None:
    line = OrderLine('o1', 'OMINOUS-MIRROR', 10)
    batch = Batch('b1', 'OMINOUS-MIRROR', 100, eta=None)
    repo = FakeRepository([batch])
    session = FakeSession()

    allocate(line, repo, session)

    assert session.committed is True
