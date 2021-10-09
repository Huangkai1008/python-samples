"""Example 1-2. A simple two-dimensional vector class.

It's simplistic for didactic reasons. It lacks proper error handling,
especially in the ``__add__`` and ``__mul__`` methods.

Examples:
    Addition::
        >>> v1 = Vector(2, 4)
        >>> v2 = Vector(2, 1)
        >>> v1 + v2
        Vector(4, 5)

    Absolute value::
        >>> v = Vector(3, 4)
        >>> abs(v)
        5.0

    Scalar multiplicaion::
        >>> v * 3
        Vector(9, 12)
        >>> abs(v * 3)
        15.0

"""

import math
from typing import Optional
from typing_extensions import Self


class Vector:
    def __init__(self, x: Optional[float] = 0, y: Optional[float] = 0) -> None:
        self.x: float = x
        self.y: float = y

    def __add__(self, other: Self) -> Self:
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar: float) -> Self:
        return Vector(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        return bool(abs(self))

    def __repr__(self) -> str:
        return f'Vector({self.x!r}, {self.y!r})'
