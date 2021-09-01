from dataclasses import dataclass

__all__ = ['Product']


@dataclass(frozen=True)
class Product:
    name: str
