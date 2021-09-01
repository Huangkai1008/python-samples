from abc import ABC, abstractmethod
from dataclasses import field
from typing import Dict

from .product import Product


class IStore(ABC):
    @abstractmethod
    def get_inventory(self, product: Product) -> int:
        ...

    @abstractmethod
    def has_enough_inventory(self, product: Product, quantity: int) -> bool:
        ...

    @abstractmethod
    def add_inventory(self, product: Product, quantity: int) -> None:
        ...

    @abstractmethod
    def remove_inventory(self, product: Product, quantity: int) -> None:
        ...


class Store(IStore):
    def __init__(self) -> None:
        self.inventory: Dict[Product, int] = field(default_factory=dict)

    def add_inventory(self, product: Product, quantity: int) -> None:
        if product in self.inventory:
            self.inventory[product] += quantity
        else:
            self.inventory[product] = quantity

    def get_inventory(self, product: Product) -> int:
        return self.inventory.get(product, 0)

    def remove_inventory(self, product: Product, quantity: int) -> None:
        if not self.has_enough_inventory(product, quantity):
            raise ValueError('Not enough inventory.')

        self.inventory[product] -= quantity

    def has_enough_inventory(self, product: Product, quantity: int) -> bool:
        return self.inventory[product] >= quantity
