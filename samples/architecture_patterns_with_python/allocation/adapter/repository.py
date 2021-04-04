from abc import ABCMeta, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session

from samples.architecture_patterns_with_python.allocation.domain.model import Product


class AbstractRepository(metaclass=ABCMeta):
    @abstractmethod
    def add(self, product: Product) -> None:
        ...

    @abstractmethod
    def get(self, sku: str) -> Optional[Product]:
        ...


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def add(self, product: Product) -> None:
        self.session.add(product)

    def get(self, sku: str) -> Optional[Product]:
        return self.session.query(Product).filter_by(sku=sku).first()
