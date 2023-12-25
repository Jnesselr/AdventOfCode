from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, combinations
from queue import Queue
from typing import TypeVar, Generic, Union, List, Callable, Dict, Optional, Set, Iterator

from aoc.util.coordinate import Coordinate, CoordinateSystem, BoundingBox
from aoc.util.graph import Graph
from aoc.util.queue import PriorityQueue

T = TypeVar('T')
U = TypeVar('U')


@dataclass(frozen=True)
class GridLocation(Generic[T]):
    coordinate: Coordinate
    item: T


@dataclass(frozen=True)
class CoordinateSteps(object):
    coordinate: Coordinate
    steps: int


class InfiniteGrid(Generic[T]):
    def __init__(self):
        self._data: Dict[Coordinate, T] = {}

    def clear(self):
        self._data = {}

    def copy(self) -> InfiniteGrid[T]:
        result: InfiniteGrid[T] = InfiniteGrid[T]()
        result._data = self._data.copy()
        return result

    def map(self, func: Callable[[T], U]) -> InfiniteGrid[U]:
        result = InfiniteGrid[U]()

        for coordinate, value in self._data.items():
            result[coordinate] = func(value)

        return result

    def __iter__(self) -> Iterator[Coordinate]:
        for data in self._data:
            yield data

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()

    @staticmethod
    def _to_coordinate(position) -> Coordinate:
        """
        We make the assumption that the grid is x right y down if they're just passing in coordinates. However, the
        user can use any coordinate system they want in an infinite grid.
        """
        if isinstance(position, tuple):
            x, y = position
            position = Coordinate(int(x), int(y), system=CoordinateSystem.X_RIGHT_Y_DOWN)
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

    def to_grid(self) -> Grid[T]:
        data = {}

        min_x = min_y = 4294967296
        max_x = max_y = -4294967296

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

    def to_graph(self, *walkable: T, directional=False) -> Graph[Coordinate]:
        walkable_coordinates = set()

        for element in walkable:
            walkable_coordinates = walkable_coordinates.union(self.find(element))

        graph: Graph[Coordinate] = Graph[Coordinate](directional=directional)

        coordinate: Coordinate
        for coordinate in walkable_coordinates:
            tests = coordinate.neighbors()

            test: Coordinate
            for test in tests:
                if test in walkable_coordinates:
                    graph.add(coordinate, test)
                    if not directional:
                        graph.add(test, coordinate)  # directional is just whether the graph is directional, we want both directions either way

        return graph

    def manhattan_graph(self, *walkable: T) -> Graph[Coordinate]:
        walkable_coordinates = set()

        for element in walkable:
            walkable_coordinates = walkable_coordinates.union(self.find(element))

        graph: Graph[Coordinate] = Graph[Coordinate](directional=False)

        first_coord: Coordinate
        second_coordinate: Coordinate
        for first_coord, second_coordinate in combinations(walkable_coordinates, 2):
            graph.add(first_coord, second_coordinate, weight=first_coord.manhattan(second_coordinate))

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
                if neighbor not in self:
                    continue

                if self[neighbor] not in walkable:
                    continue

                new_cost = cost_so_far[current] + 1

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heuristic_cost = abs(end.y - neighbor.y) + (end.x - neighbor.x)
                    priority = new_cost + heuristic_cost

                    frontier.push(neighbor, priority)
                    came_from[neighbor] = current

    def flood_fill(self, starting_coordinate: Coordinate, current_item: T, new_item: T):
        q = Queue()
        seen: set[Coordinate] = set()
        q.put(starting_coordinate)
        seen.add(starting_coordinate)

        while not q.empty():
            coordinate = q.get()
            self._data[coordinate] = new_item

            for neighbor in coordinate.neighbors():
                if neighbor in seen:
                    continue  # We've already seen it

                if neighbor not in self._data:
                    continue  # We don't have it in our grid

                if self._data[neighbor] != current_item:
                    continue  # It's not the item we're looking for

                q.put(neighbor)
                seen.add(neighbor)

    def flood_map(self,
                  start: Coordinate,
                  *walkable,
                  max_value: Optional[int] = None
                  ) -> Dict[Coordinate, int]:
        result: Dict[Coordinate, int] = {}

        if self[start] in walkable:
            result[start] = 0

        queue: PriorityQueue[CoordinateSteps] = PriorityQueue[CoordinateSteps]()
        queue.push(CoordinateSteps(coordinate=start, steps=0), 0)

        while queue:
            item: CoordinateSteps = queue.pop()

            new_steps = item.steps + 1
            if max_value is not None and new_steps > max_value:
                continue

            for neighbor in item.coordinate.neighbors():
                if neighbor not in self:
                    continue

                if neighbor in result:
                    continue

                if self[neighbor] not in walkable:
                    continue

                queue.push(CoordinateSteps(neighbor, new_steps), new_steps)
                result[neighbor] = new_steps

        return result

    def __getitem__(self, position) -> Optional[T]:
        position = self._to_coordinate(position)

        if position in self:
            return self._data[position]
        return None

    def __setitem__(self, position, item):
        position = self._to_coordinate(position)

        self._data[position] = item

    def __delitem__(self, position):
        position = self._to_coordinate(position)

        if position in self:
            del self._data[position]

    def __contains__(self, position):
        position = self._to_coordinate(position)

        return position in self._data

    @property
    def bounding_box(self) -> BoundingBox:
        return BoundingBox().expand(*self._data.keys())

    def find(self, test: Union[T, Callable]) -> List[Coordinate]:
        result = []

        for coordinate, item in self._data.items():
            if callable(test):
                if test(item):
                    result.append(coordinate)
            elif item == test:
                result.append(coordinate)

        return result

    def neighbor_count(self, coordinate: Coordinate, test: Union[T, Callable]) -> int:
        result = 0

        for neighbor in coordinate.neighbors():
            if neighbor not in self:
                continue
            item = self._data[neighbor]
            if callable(test):
                if test(item):
                    result += 1
            elif item == test:
                result += 1

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

    def cut(self, bounding_box: BoundingBox) -> Grid[T]:
        new_width = bounding_box.max_x - bounding_box.min_x + 1
        new_height = bounding_box.max_y - bounding_box.min_y + 1
        new_grid = Grid[T](new_width, new_height)

        for row in range(new_height):
            for col in range(new_width):
                old_coordinate = Coordinate(
                    col + bounding_box.min_x,
                    row + bounding_box.min_y,
                    system=CoordinateSystem.X_RIGHT_Y_DOWN
                )
                new_coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)

                new_grid[new_coordinate] = self[old_coordinate]

        return new_grid

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

    def fill_empty(self, item: T):
        for row in range(self.height):
            for col in range(self.width):
                coordinate = Coordinate(col, row, system=CoordinateSystem.X_RIGHT_Y_DOWN)

                if coordinate not in self._data:
                    self._data[coordinate] = item

    def fill_from_edges(self, to_replace: T, new_item: T):
        for coordinate in self.find(to_replace):
            if not coordinate.x == 0 and \
                    not coordinate.y == 0 and \
                    not coordinate.x == self.width - 1 and \
                    not coordinate.y == self.height - 1:
                continue  # Not on the edge, don't want to risk grabbing an inside one

            if self[coordinate] != to_replace:  # Changed by a previous flood fill
                continue

            self.flood_fill(coordinate, to_replace, new_item)

    def replace(self, to_replace: T, new_item: T):
        for coordinate in self.find(to_replace):
            self[coordinate] = new_item

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

    def flip_horizontal(self) -> Grid[str]:
        result: Grid[T] = Grid[T](self.width, self.height)

        for row in range(self.height):
            for col in range(self.width):
                result[self.width - col - 1, row] = self[col, row]

        return result

    def flip_vertical(self) -> Grid[str]:
        result: Grid[T] = Grid[T](self.width, self.height)

        for row in range(self.height):
            for col in range(self.width):
                result[col, self.height - row - 1] = self[col, row]

        return result

    def rotate_right(self) -> Grid[str]:
        result: Grid[T] = Grid[T](width=self.height, height=self.width)

        for row in range(self.height):
            for col in range(self.width):
                result[self.height - row - 1, col] = self[col, row]

        return result


class MagicGrid(InfiniteGrid[T]):
    def __init__(self, magic_function: Callable[[MagicGrid[T], Coordinate], T]):
        super().__init__()
        self._magic_function = magic_function

    def __getitem__(self, position) -> Optional[T]:
        position = self._to_coordinate(position)

        if position in self._data:
            return self._data[position]

        result = self._magic_function(self, position)
        if result is not None:
            self._data[position] = result
            return result

        return None

    def __contains__(self, position):
        position = self._to_coordinate(position)

        result = self._magic_function(self, position)

        return result is not None
