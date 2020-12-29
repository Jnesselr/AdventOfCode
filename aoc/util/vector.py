from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Vector(object):
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other: Union[Vector, int]) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return Vector(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other: Union[Vector, int]) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return Vector(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other: Union[Vector, int]) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vector(self.x * other, self.y * other, self.z * other)

    def __floordiv__(self, other: Union[Vector, int]) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x // other.x, self.y // other.y, self.z // other.z)
        else:
            return Vector(self.x // other, self.y // other, self.z // other)

    def __rmul__(self, other) -> Vector:
        return self.__mul__(other)

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y, -self.z)

    def __lt__(self, other: Vector):
        diff = (self - other).signs()
        for element in [diff.x, diff.y, diff.z]:
            if element == -1:
                return True
            elif element == 0:
                continue
            elif element == 1:
                return False

        return False

    def __abs__(self):
        return Vector(abs(self.x), abs(self.y), abs(self.z))

    def distance(self, other: Vector):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def signs(self):
        return Vector(
            x=0 if self.x == 0 else (self.x // abs(self.x)),
            y=0 if self.y == 0 else (self.y // abs(self.y)),
            z=0 if self.z == 0 else (self.z // abs(self.z))
        )