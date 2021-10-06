from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, NamedTuple, Optional, Sequence


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity


@dataclass(frozen=True)
class Order:
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional[Callable[['Order'], Decimal]] = None

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self) -> str:
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'


Promotion = Callable[[Order], Decimal]
promos: list[Promotion] = []


def promotion(promo: Promotion) -> Promotion:
    promos.append(promo)
    return promo


def best_promo(order: Order) -> Decimal:
    """Select best discount available."""
    return max(promo(order) for promo in promos)


@promotion
def fidelity_promo(order: Order) -> Decimal:
    """5% discount for customers with 1000 or more fidelity points."""
    rate = Decimal('0.05')
    if order.customer.fidelity >= 1000:
        return order.total() * rate
    return Decimal(0)


@promotion
def bulk_item_promo(order: Order) -> Decimal:
    """10% discount for each LineItem with 20 or more units."""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


@promotion
def large_order_promo(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items."""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)
