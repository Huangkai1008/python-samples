from dataclasses import dataclass, field
from typing import Dict

from samples.unit_testing_pattern.product import Product

__all__ = ['Store']


@dataclass
class Store:
    inventory: Dict[Product, int] = field(default_factory=dict)

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
