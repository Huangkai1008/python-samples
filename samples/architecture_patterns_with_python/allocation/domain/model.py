from dataclasses import dataclass
from datetime import date
from typing import Any, List, Optional, Set

from samples.architecture_patterns_with_python.allocation.domain.command import Allocate
from samples.architecture_patterns_with_python.allocation.domain.event import OutOfStock
from samples.architecture_patterns_with_python.allocation.services.message_bus import (
    Message,
)


# `Frozen=True` is used in the original book, and I personally prefer this scheme.
# But SQLALCHEMY causes https://github.com/cosmicpython/code/issues/17.
#
# The recommended solution is https://stackoverflow.com/questions/61419449.
# But I don't think this is a clean approach, so I use `unsafe_hash=True` to resolve it.
@dataclass(unsafe_hash=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int


class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date] = None
    ) -> None:
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_qty = qty
        self._allocations: Set[OrderLine] = set()

    @property
    def allocated_qty(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_qty(self) -> int:
        return self._purchased_qty - self.allocated_qty

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocations:
            self._allocations.remove(line)

    def deallocate_one(self) -> OrderLine:
        return self._allocations.pop()

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_qty >= line.qty

    def __repr__(self) -> str:
        return f'<Batch {self.reference}>'

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other: Any) -> bool:
        if self.eta is None:
            return False
        if not isinstance(other, Batch) or other.eta is None:
            return True
        return self.eta > other.eta

    def __lt__(self, other: Any) -> bool:
        if self.eta is None:
            return True
        if not isinstance(other, Batch) or other.eta is None:
            return False
        return self.eta < other.eta


class Product:
    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0) -> None:
        self.sku: str = sku
        self.batches: List[Batch] = batches
        self.version_number: int = version_number
        self.events: List[Message] = []

    def allocate(self, line: OrderLine) -> Optional[str]:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            self.version_number += 1
            return batch.reference
        except StopIteration:
            self.events.append(OutOfStock(self.sku))
            return None

    def change_batch_quantity(self, ref: str, qty: int) -> None:
        batch = next(b for b in self.batches if b.reference == ref)
        batch._purchased_qty = qty
        while batch.available_qty < 0:
            line = batch.deallocate_one()
            self.events.append(Allocate(line.order_id, line.sku, line.qty))
