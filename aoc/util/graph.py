from __future__ import annotations
from dataclasses import dataclass
from typing import TypeVar, Generic, Dict, Optional, Set, List, Callable

from aoc.util.coordinate import Coordinate
from aoc.util.queue import PriorityQueue

T = TypeVar('T')
U = TypeVar('U')


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
        return start.manhattan(end)


@dataclass(frozen=True)
class WithSteps(Generic[T]):
    value: T
    steps: int
    path: List[T]


class Graph(Generic[T]):
    def __init__(self, directional=False):
        self._edges = set()
        self._nodes = {}
        self._directional = directional

    def add(self, start: T, end: T, weight=1):
        forward = Edge(start, end, weight)
        self._edges.add(forward)
        self._nodes.setdefault(start, set()).add(forward)

        if not self._directional:
            back = Edge(end, start, weight)
            self._edges.add(back)
            self._nodes.setdefault(end, set()).add(back)

    def merge(self, graph: Graph[T]) -> Graph[T]:
        for edge in graph._edges:
            self.add(edge.start, edge.end, edge.weight)

        return self

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

    def flood_find(self, start: T, end: T):
        queue: PriorityQueue[WithSteps[T]] = PriorityQueue[WithSteps[T]]()
        seen: Set[T] = set()
        queue.push(WithSteps(value=start, steps=0, path=[start]), 0)

        while queue:
            item: WithSteps[T] = queue.pop()

            if item.value == end:
                return item.path

            for edge in self._nodes.setdefault(item.value, []):
                neighbor: T = edge.end
                if neighbor in seen:
                    continue

                seen.add(neighbor)
                new_path = item.path.copy()
                new_path.append(neighbor)
                new_steps = item.steps + 1
                queue.push(WithSteps(value=neighbor, steps=new_steps, path=new_path), new_steps)

        return None

    def map(self, func: Callable[[T], U]) -> Graph[U]:
        new_graph: Graph[U] = Graph[U](directional=self._directional)

        for edge in self._edges:
            new_graph.add(func(edge.start), func(edge.end), edge.weight)

        return new_graph
