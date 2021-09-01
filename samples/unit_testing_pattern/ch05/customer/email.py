from typing import Protocol


class EmailGateway(Protocol):
    def send_receipt(self, email: str, product_name: str, quantity: int) -> None:
        ...
