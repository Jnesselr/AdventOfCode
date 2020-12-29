from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Vector(object):
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance(self, other: Vector):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def signs(self):
        return Vector(
            x=0 if self.x == 0 else (self.x // abs(self.x)),
            y=0 if self.y == 0 else (self.y // abs(self.y)),
            z=0 if self.z == 0 else (self.z // abs(self.z))
        )