from typing import Protocol

__all__ = ['Database']


class Database(Protocol):
    def get_number_of_users(self) -> int:
        ...
