from typing import Callable, List, Type

from samples.architecture_patterns_with_python.allocation.adapter import email
from samples.architecture_patterns_with_python.allocation.domain.event import (
    Event,
    OutOfStock,
)


def handle(event: Event) -> None:
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_out_of_stock_notification(event: OutOfStock) -> None:
    email.send_mail("stock@made.com", f'Out of Stock for {event.sku}')


HANDLERS: dict[Type[Event], List[Callable]] = {
    OutOfStock: [send_out_of_stock_notification],
}
