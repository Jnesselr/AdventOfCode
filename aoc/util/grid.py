from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Generic, Union, List, Callable, Dict, Optional

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.graph import Graph
from aoc.util.queue import PriorityQueue

T = TypeVar('T')


@dataclass(frozen=True)
class GridLocation(Generic[T]):
    coordinate: Coordinate
    item: T


class InfiniteGrid(Generic[T]):
    def __init__(self):
        self._data = {}

    def clear(self):
        self._data = {}

    def copy(self) -> InfiniteGrid[T]:
        result: InfiniteGrid[T] = InfiniteGrid[T]()
        result._data = self._data.copy()
        return result

    def __iter__(self) -> Coordinate:
        for data in self._data:
            yield data

    def items(self):
        return self._data.items()

    @staticmethod
    def _to_coordinate(position) -> Coordinate:
        """
        We make the assumption that the grid is x right y down if they're just passing in coordinates. However, the
        user can use any coordinate system they want in an infinite grid.
        """
        if isinstance(position, tuple):
            x, y = position
            position = Coordinate(x, y, system=CoordinateSystem.X_RIGHT_Y_DOWN)
        return position

    @property
    def max_x(self):
        return max(map(lambda coord: coord.x, self._data.keys()))

    @property
    def min_x(self):
        return min(map(lambda coord: coord.x, self._data.keys()))

    @property
    def max_y(self):
        return max(map(lambda coord: coord.y, self._data.keys()))

    @property
    def min_y(self):
        return min(map(lambda coord: coord.y, self._data.keys()))

    # TODO This makes assumptions about the coordinate system. It assumes X_RIGHT_Y_UP.
    def to_grid(self) -> Grid[T]:
        data = {}

        min_x = min_y = 4294967296
        max_x = max_y = 0

        for coordinate, item in self._data.items():
            x = coordinate.x
            y = coordinate.y
            if coordinate.system == CoordinateSystem.X_RIGHT_Y_DOWN:
                y = -y

            coordinate = Coordinate(x, y, system=CoordinateSystem.X_RIGHT_Y_UP)
            data[coordinate] = item

            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        result = Grid[T](width, height)
        for coordinate, item in data.items():
            result[coordinate.x - min_x, max_y - coordinate.y] = item

        return result

    def to_graph(self, *walkable: T) -> Graph[Coordinate]:
        walkable_coordinates = set()

        for element in walkable:
            walkable_coordinates = walkable_coordinates.union(self.find(element))

        graph: Graph[Coordinate] = Graph[Coordinate]()

        coordinate: Coordinate
        for coordinate in walkable_coordinates:
            tests = coordinate.neighbors()

            test: Coordinate
            for test in tests:
                if test in walkable_coordinates:
                    graph.add(coordinate, test)

        return graph

    def find_path(self, start: Coordinate, end: Coordinate, *walkable: T):
        frontier: PriorityQueue[Coordinate] = PriorityQueue[Coordinate]()
        frontier.push(start, 0)
        came_from: Dict[Coordinate, Optional[Coordinate]] = {}
        cost_so_far: Dict[Coordinate, int] = {}

        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current: Coordinate = frontier.pop()

            if current == end:
                source = end
                result = []

                while source is not None:
                    result.insert(0, source)
                    source = came_from[source]

                return result

            for neighbor in current.neighbors():
                if neighbor not in self._data:
                    continue

                if self._data[neighbor] not in walkable:
                    continue

                new_cost = cost_so_far[current] + 1

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heuristic_cost = abs(end.y - neighbor.y) + (end.x - neighbor.x)
                    priority = new_cost + heuristic_cost

                    frontier.push(neighbor, priority)
                    came_from[neighbor] = current

    def __getitem__(self, position) -> Optional[T]:
        position = self._to_coordinate(position)

        if position in self._data:
            return self._data[position]
        return None

    def __setitem__(self, position, item):
        position = self._to_coordinate(position)

        self._data[position] = item

    def __contains__(self, position):
        position = self._to_coordinate(position)

        return position in self._data

    def find(self, test: Union[T, Callable]) -> List[Coordinate]:
        result = []

        for coordinate, item in self._data.items():
            if callable(test):
                if test(item):
                    result.append(coordinate)
            elif item == test:
                result.append(coordinate)

        return result


# TODO Add constraints for setting/getting position to be in bounds
class Grid(InfiniteGrid[T]):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

    def copy(self) -> Grid[T]:
        result: Grid[T] = Grid[T](self.width, self.height)
        result._data = self._data.copy()
        return result

    @staticmethod
    def from_str(lines: Union[str, List[str]]) -> Grid[str]:
        if isinstance(lines, str):
            lines = lines.rstrip('\n').split('\n')

        width = len(max(lines, key=len))
        height = len(lines)

        grid: Grid[str] = Grid[str](width, height)

        for row in range(len(lines)):
            line = lines[row]
            for col in range(len(line)):
                grid[col, row] = line[col]

        return grid

    def fill(self, item: T):
        for row in range(self.height):
            for col in range(self.width):
                coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)

                self._data[coordinate] = item

    # TODO Add a key function for items that aren't characters
    # TODO Add a default character to use if the coordinate isn't in there
    def print(self, key=None, not_found=' '):
        if key is None:
            def key(item):
                return item[0]

        for row in range(self.height):
            line = ""
            for col in range(self.width):
                coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)

                if coordinate in self._data:
                    line += key(self._data[coordinate])
                else:
                    line += not_found

            print(line)
