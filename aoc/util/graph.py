from __future__ import annotations

import enum
from dataclasses import dataclass
from pathlib import Path
from queue import Queue
from typing import TypeVar, Generic, Dict, Optional, Set, List, Callable, FrozenSet

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


@dataclass(frozen=True)
class SearchAttempt(object):
    total_weight: int
    start: str
    current: str
    visited: FrozenSet[str]


class CompressionWhatToKeep(enum.Enum):
    LOWEST = enum.auto()
    HIGHEST = enum.auto()
    ALL = enum.auto()


class Graph(Generic[T]):
    def __init__(self, directional=False):
        self._all_nodes = set()
        self._edges = set()
        self._forward_nodes: dict[T, set[Edge[T]]] = {}
        self._back_nodes: dict[T, set[Edge[T]]] = {}
        self._directional: bool = directional

    @property
    def all_nodes(self) -> Set[T]:
        return set(self._all_nodes)

    @property
    def all_edges(self) -> Set[Edge[T]]:
        return set(self._edges)

    def add(self, start: T, end: T, weight=1):
        self._all_nodes.add(start)
        self._all_nodes.add(end)

        forward = Edge(start, end, weight)
        self._edges.add(forward)
        self._forward_nodes.setdefault(start, set()).add(forward)
        self._back_nodes.setdefault(end, set()).add(forward)

        if not self._directional:
            back = Edge(end, start, weight)
            self._edges.add(back)
            self._forward_nodes.setdefault(end, set()).add(back)
            self._back_nodes.setdefault(start, set()).add(back)

    def remove_node_link(self, start: T, end: T):
        edges_to_murder = set()
        if start in self._forward_nodes:
            for edge in self._forward_nodes[start]:
                if edge.end == end:
                    edges_to_murder.add(edge)

        if end in self._back_nodes:
            for edge in self._back_nodes[end]:
                if edge.start == start:
                    edges_to_murder.add(edge)

        self._murder_edges(edges_to_murder)

    def remove(self, node: T):
        if node in self._all_nodes:
            self._all_nodes.remove(node)

        edges_to_murder = set()
        if node in self._forward_nodes:
            for edge in self._forward_nodes[node]:
                edges_to_murder.add(edge)

        if node in self._back_nodes:
            for edge in self._back_nodes[node]:
                edges_to_murder.add(edge)

        self._murder_edges(edges_to_murder)

    def _murder_edges(self, edges_to_murder):
        for edge in edges_to_murder:
            self._edges.remove(edge)
            if edge.start in self._forward_nodes:
                if edge in self._forward_nodes[edge.start]:
                    self._forward_nodes[edge.start].remove(edge)

                    if len(self._forward_nodes[edge.start]) == 0:
                        del self._forward_nodes[edge.start]
            if edge.start in self._back_nodes:
                if edge in self._back_nodes[edge.start]:
                    self._back_nodes[edge.start].remove(edge)

                    if len(self._back_nodes[edge.start]) == 0:
                        del self._back_nodes[edge.start]

            if edge.end in self._forward_nodes:
                if edge in self._forward_nodes[edge.end]:
                    self._forward_nodes[edge.end].remove(edge)

                    if len(self._forward_nodes[edge.start]) == 0:
                        del self._forward_nodes[edge.start]
            if edge.end in self._back_nodes:
                if edge in self._back_nodes[edge.end]:
                    self._back_nodes[edge.end].remove(edge)

                    if len(self._back_nodes[edge.end]) == 0:
                        del self._back_nodes[edge.end]

    def nodes_to(self, end: T) -> Set[T]:
        if end not in self._back_nodes:
            return set()

        return set(edge.start for edge in self._back_nodes[end])

    def nodes_from(self, start: T) -> Set[T]:
        if start not in self._forward_nodes:
            return set()

        return set(edge.end for edge in self._forward_nodes[start])

    def edges_to(self, end: T) -> Set[Edge[T]]:
        if end not in self._back_nodes:
            return set()

        return set(self._back_nodes[end])

    def edges_from(self, start: T) -> Set[Edge[T]]:
        if start not in self._forward_nodes:
            return set()

        return set(self._forward_nodes[start])

    def merge(self, graph: Graph[T]) -> Graph[T]:
        for edge in graph._edges:
            self.add(edge.start, edge.end, edge.weight)

        return self

    def get_weight(self, path: list[T]) -> int:
        result = 0

        for i in range(len(path) - 1):
            start: T = path[i]
            end: T = path[i + 1]

            common_edges = self.edges_to(end).intersection(self.edges_from(start))
            if len(common_edges) == 0:
                raise ValueError("Could not find common edge between start and end")

            if len(common_edges) > 1:
                raise ValueError("Too many edges? Maybe not an issue?")

            result += list(common_edges)[0].weight

        return result

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
            for edge in self._forward_nodes.setdefault(current, set()):
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

            for edge in self._forward_nodes.setdefault(item.value, set()):
                neighbor: T = edge.end
                if neighbor in seen:
                    continue

                seen.add(neighbor)
                new_path = item.path.copy()
                new_path.append(neighbor)
                new_steps = item.steps + 1
                queue.push(WithSteps(value=neighbor, steps=new_steps, path=new_path), new_steps)

        return None

    def flood_find_max(self, start: T, end: T) -> List[T]:
        queue: Queue = Queue()
        queue.put(WithSteps(value=start, steps=0, path=[start]))  # edge is weight here

        longest_path: Optional[WithSteps] = None

        while not queue.empty():
            item: WithSteps[T] = queue.get()

            if item.value == end:
                if longest_path is None or longest_path.steps < item.steps:
                    # print(item.steps, queue.qsize())
                    longest_path = item
                continue

            for edge in self._forward_nodes.setdefault(item.value, set()):
                neighbor: T = edge.end
                if neighbor in item.path:
                    continue

                new_path = item.path.copy()
                new_path.append(neighbor)
                new_steps = item.steps + edge.weight
                queue.put(WithSteps(value=neighbor, steps=new_steps, path=new_path))

        return longest_path.path

    def map(self, func: Callable[[T], U]) -> Graph[U]:
        new_graph: Graph[U] = Graph[U](directional=self._directional)

        for edge in self._edges:
            new_graph.add(func(edge.start), func(edge.end), edge.weight)

        return new_graph

    def sorted(self):
        edges = self._edges.copy()
        has_incoming = set(edge.end for edge in self._edges)
        no_incoming = set(self._forward_nodes.keys()) - has_incoming

        while len(no_incoming) > 0:
            next_element = min(no_incoming)
            yield next_element
            no_incoming.remove(next_element)

            for edge in edges.copy():
                if edge.start != next_element:
                    continue

                edges.remove(edge)

                if len([x for x in edges if x.end == edge.end]) == 0:
                    no_incoming.add(edge.end)

    def tsp(self) -> int:
        queue: PriorityQueue[SearchAttempt] = PriorityQueue[SearchAttempt]()

        for node in self._all_nodes:
            queue.push(SearchAttempt(0, node, node, frozenset({node})), 0)

        while not queue.empty:
            search: SearchAttempt = queue.pop()

            if search.visited == self._all_nodes:
                return search.total_weight

            for edge in self.edges_from(search.current):
                if edge.end in search.visited:
                    continue

                new_distance = search.total_weight + edge.weight
                new_visited = frozenset(search.visited.union({edge.end}))
                new_search = SearchAttempt(new_distance, search.start, edge.end, new_visited)

                queue.push(new_search, new_distance)

    def highest_tsp(self, loop=False):
        queue = Queue()

        starting_nodes = list(self._all_nodes)

        # If this is a loop, then just pick one to start with
        if loop:
            starting_nodes = [starting_nodes.pop()]

        for node in starting_nodes:
            queue.put(SearchAttempt(0, node, node, frozenset({node})))

        result = 0

        while not queue.empty():
            search: SearchAttempt = queue.get()

            if search.visited == self._all_nodes:
                if loop and search.start != search.current:
                    edges = [e for e in self.edges_from(search.current) if e.end == search.start]

                    if len(edges) > 0:
                        weight = edges.pop().weight
                        result = max(search.total_weight + weight, result)
                else:
                    result = max(search.total_weight, result)

            for edge in self.edges_from(search.current):
                if edge.end in search.visited:
                    continue

                new_distance = search.total_weight + edge.weight
                new_visited = frozenset(search.visited.union({edge.end}))
                new_search = SearchAttempt(new_distance, search.start, edge.end, new_visited)

                queue.put(new_search)

        return result

    def compress(self, *what_to_keep: T, keep_logic: CompressionWhatToKeep = CompressionWhatToKeep.LOWEST):
        what_to_keep = set(what_to_keep)
        for node in set(self._all_nodes):
            if node in what_to_keep:
                continue

            edges_to = self.edges_to(node)
            edges_from = self.edges_from(node)

            # If we have duplicate edges, pick the lowest weighted one
            min_max_weight: Dict[tuple[T, T], int] = {}
            to_keep: list[tuple[T, T, int]] = []

            edge_to: Edge[T]
            for edge_to in edges_to:
                edge_from: Edge[T]
                for edge_from in edges_from:
                    if edge_to.start == edge_from.end:
                        continue
                    new_weight = edge_to.weight + edge_from.weight
                    edge_tuple = edge_to.start, edge_from.end
                    with_weight_t = edge_to.start, edge_from.end, new_weight

                    if keep_logic == CompressionWhatToKeep.ALL:
                        to_keep.append(with_weight_t)
                    elif edge_tuple not in min_max_weight:
                        min_max_weight[edge_tuple] = new_weight
                        to_keep = [with_weight_t]
                    elif keep_logic == CompressionWhatToKeep.LOWEST and min_max_weight[edge_tuple] > new_weight:
                        min_max_weight[edge_tuple] = new_weight
                        to_keep = [with_weight_t]
                    elif keep_logic == CompressionWhatToKeep.HIGHEST and min_max_weight[edge_tuple] < new_weight:
                        min_max_weight[edge_tuple] = new_weight
                        to_keep = [with_weight_t]

            for edge_tuple in to_keep:
                start, end, weight = edge_tuple
                self.add(start, end, weight=weight)

            self.remove(node)

    def interconnect(self):
        @dataclass
        class InterconnectResult(Generic[T]):
            node: T
            current_weight: int

        for node in set(self._all_nodes):
            q = Queue()
            weight_map: Dict[str, int] = {
                node: 0
            }
            for edge in self.edges_from(node):
                q.put(InterconnectResult(
                    node=edge.end,
                    current_weight=edge.weight
                ))
                weight_map[edge.end] = edge.weight

            while not q.empty():
                result: InterconnectResult = q.get()
                for edge in self.edges_from(result.node):
                    new_weight = result.current_weight + edge.weight
                    if edge.end in weight_map and weight_map[edge.end] <= new_weight:
                        continue

                    weight_map[edge.end] = new_weight
                    q.put(InterconnectResult(
                        node=edge.end,
                        current_weight=new_weight
                    ))

            nodes_from = self.nodes_from(node)
            for end, weight in weight_map.items():
                if end == node:
                    continue  # This is us

                if end in nodes_from:
                    continue  # Already exists as a direct connection
                self.add(node, end, weight)

    def dotviz(self, file_name: str):
        with Path(file_name).open('w') as fh:
            if self._directional:
                fh.write("digraph {\n")
            else:
                fh.write("graph {\n")

            for node in self._all_nodes:
                for other_node in self.nodes_from(node):
                    if self._directional:
                        fh.write(f"{node} -> {other_node};\n")
                    else:
                        fh.write(
                            f"{node} -- {other_node};\n")  # TODO Handle the fact that there's an edge in the other direction

            fh.write("}")

    def separate(self):
        nodes: set[T] = set(self._all_nodes)
        while len(nodes) > 0:
            starting_node: T = nodes.pop()
            graph: Graph[T] = Graph(directional=True)
            q: Queue = Queue()
            q.put(starting_node)

            while not q.empty():
                node: T = q.get()

                for edge in self.edges_from(node):
                    graph.add(node, edge.end, weight=edge.weight)
                    if edge.end in nodes:
                        q.put(edge.end)
                        nodes.remove(edge.end)

                for edge in self.edges_to(node):
                    graph.add(edge.start, node, weight=edge.weight)
                    if edge.start in nodes:
                        q.put(edge.start)
                        nodes.remove(edge.start)

            yield graph

    def subgraph(self, starting_node: T) -> Graph:
        result = Graph[T](directional=self._directional)

        seen: set[Edge[T]] = {starting_node}
        to_check: list[T] = [starting_node]

        while len(to_check) > 0:
            node: T = to_check.pop()

            next_edges: set[Edge[T]] = self.edges_from(node)
            for edge in next_edges:
                if edge in seen:
                    continue

                to_check.append(edge.end)
                seen.add(edge)
                result.add(edge.start, edge.end, edge.weight)

        return result
