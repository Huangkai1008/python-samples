from typing import Protocol

__all__ = ['EmailGateway']


class EmailGateway(Protocol):
    def send_greetings_email(self, user_email: str) -> None:
        ...
