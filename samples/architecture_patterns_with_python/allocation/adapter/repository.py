from typing import Optional, Protocol, Set

from sqlalchemy.orm import Session

from samples.architecture_patterns_with_python.allocation.adapter.orm import batch
from samples.architecture_patterns_with_python.allocation.domain.model import (
    Batch,
    Product,
)


class AbstractRepository(Protocol):
    seen: Set[Product]

    def add(self, product: Product) -> None:
        ...

    def get(self, sku: str) -> Optional[Product]:
        ...

    def get_by_batch_ref(self, batch_ref: str) -> Optional[Product]:
        ...


class SQLAlchemyRepository:
    seen: Set[Product]

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def add(self, product: Product) -> None:
        self.session.add(product)

    def get(self, sku: str) -> Optional[Product]:
        return self.session.query(Product).filter_by(sku=sku).first()

    def get_by_batch_ref(self, batch_ref: str) -> Optional[Product]:
        return (
            self.session.query(Product)
            .join(Batch)
            .filter(batch.c.reference == batch_ref)
            .first()
        )


class ProductRepository:
    seen: Set[Product]

    def __init__(self, repo: AbstractRepository) -> None:
        self.seen: Set[Product] = set()
        self._repo: AbstractRepository = repo

    def add(self, product: Product) -> None:
        self._repo.add(product)
        self.seen.add(product)

    def get(self, sku: str) -> Optional[Product]:
        product = self._repo.get(sku)
        if product:
            self.seen.add(product)
        return product

    def get_by_batch_ref(self, batch_ref: str) -> Optional[Product]:
        product = self._repo.get_by_batch_ref(batch_ref)
        if product:
            self.seen.add(product)
        return product
