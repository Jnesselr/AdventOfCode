from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate(object):
    """
    The notation for this is:
     +X is to the right
     -X is to the left
     +Y is up
     -Y is down
    """
    x: int
    y: int

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def right(self):
        return Coordinate(self.x + 1, self.y)

    def left(self):
        return Coordinate(self.x - 1, self.y)

    def up(self):
        return Coordinate(self.x, self.y + 1)

    def down(self):
        return Coordinate(self.x, self.y - 1)
