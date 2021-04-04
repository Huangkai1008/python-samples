from typing import Iterable, Optional, Set

import pytest

from samples.architecture_patterns_with_python.allocation.adapter.repository import (
    AbstractRepository,
)
from samples.architecture_patterns_with_python.allocation.domain.model import (
    Batch,
    Product,
)
from samples.architecture_patterns_with_python.allocation.services import service
from samples.architecture_patterns_with_python.allocation.services.service import (
    InvalidSKU,
    allocate,
)
from samples.architecture_patterns_with_python.allocation.services.unit_of_work import (
    AbstractUnitOfWork,
)


class FakeRepository(AbstractRepository):
    def __init__(self, products: Iterable[Product]) -> None:
        self._products: Set[Product] = set(products)

    def add(self, product: Product) -> None:
        self._products.add(product)

    def get(self, sku: str) -> Optional[Product]:
        return next((p for p in self._products if p.sku == sku), None)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.products = FakeRepository([])
        self.committed: bool = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass


def test_add_batch_for_new_product() -> None:
    uow = FakeUnitOfWork()

    service.add_batch('b1', 'COMPLICATED-LAMP', 100, None, uow)

    assert uow.products.get('COMPLICATED-LAMP') is not None
    assert uow.committed


def test_add_batch_for_existing_product() -> None:
    uow = FakeUnitOfWork()

    service.add_batch('b1', 'GARISH-RUG', 100, None, uow)
    service.add_batch('b2', 'GARISH-RUG', 99, None, uow)

    assert 'b2' in [b.reference for b in uow.products.get('GARISH-RUG').batches]


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
