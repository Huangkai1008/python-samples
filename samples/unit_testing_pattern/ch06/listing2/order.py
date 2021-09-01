from dataclasses import dataclass, field
from typing import List

from .product import Product


@dataclass
class Order:
    products: List[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)
