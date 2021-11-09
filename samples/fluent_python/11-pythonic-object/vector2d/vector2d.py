import math
from array import array
from typing import Generator


class Vector2d:
    typecode = 'd'

    def __init__(self, x: float, y: float) -> None:
        self._x: float = x
        self._y: float = y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __iter__(self) -> Generator[float, None, None]:
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return '{}({!r}, {!r})'.format(type(self).__name__, *self)

    def __str__(self) -> str:
        return str(tuple(self))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector2d):
            return tuple(self) == tuple(other)
        return NotImplemented

    def __bytes__(self) -> bytes:
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        return bool(abs(self))

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    @classmethod
    def from_bytes(cls, octets: bytes) -> 'Vector2d':
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
