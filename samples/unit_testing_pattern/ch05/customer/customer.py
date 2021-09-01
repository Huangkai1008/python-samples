from dataclasses import dataclass

from .product import Product
from .store import IStore


@dataclass
class Customer:
    id: int
    email: str

    @classmethod
    def purchase(cls, store: IStore, product: Product, quantity: int) -> bool:
        if not store.has_enough_inventory(product, quantity):
            return False

        store.remove_inventory(product, quantity)
        return True
