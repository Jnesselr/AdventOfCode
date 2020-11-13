from dataclasses import dataclass
from typing import TypeVar, Generic, Dict, Optional

from aoc.util.coordinate import Coordinate
from aoc.util.queue import PriorityQueue

T = TypeVar('T')


@dataclass(frozen=True)
class Edge(Generic[T]):
    start: T
    end: T
    weight: int = 1


class Heuristic(Generic[T]):
    def __call__(self, start: T, end: T) -> int:
        pass


class CoordinateHeuristic(Heuristic[Coordinate]):
    def __call__(self, start: Coordinate, end: Coordinate) -> int:
        return abs(end.y - start.y) + (end.x - start.x)


class Graph(Generic[T]):
    def __init__(self, directional=False):
        self._edges = set()
        self._nodes = {}
        self._directional = directional

    def add(self, start: T, end: T, weight = 1):
        forward = Edge(start, end, weight)
        self._edges.add(forward)
        self._nodes.setdefault(start, set()).add(forward)

        if not self._directional:
            back = Edge(end, start, weight)
            self._edges.add(back)
            self._nodes.setdefault(end, set()).add(back)

    def find_path(self, start: T, end: T, heuristic: Heuristic[T]):
        frontier: PriorityQueue[T] = PriorityQueue[T]()
        frontier.push(start, 0)
        came_from: Dict[T, Optional[T]] = {}
        cost_so_far: Dict[T, int] = {}

        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current: T = frontier.pop()

            if current == end:
                source = end
                result = []

                while source is not None:
                    result.insert(0, source)
                    source = came_from[source]

                return result

            edge: Edge[T]
            for edge in self._nodes.setdefault(current, []):
                neighbor = edge.end
                new_cost = cost_so_far[current] + edge.weight

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, end)

                    frontier.push(neighbor, priority)
                    came_from[neighbor] = current

        return None
