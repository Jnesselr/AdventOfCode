import re
from dataclasses import dataclass
from queue import Queue
from typing import FrozenSet

from aoc.util.graph import Graph
from aoc.util.inputs import Input
from aoc.util.queue import PriorityQueue


@dataclass(frozen=True)
class SearchAttempt(object):
    distance: int
    current: str
    visited: FrozenSet[str]


class Y2015D9(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        all_cities = set()
        self.graph: Graph[str] = Graph[str]()

        for line in lines:
            matched = re.match(r'(\w+) to (\w+) = (\d+)', line)

            _from = matched.group(1)
            _to = matched.group(2)
            self.graph.add(_from, _to, weight=int(matched.group(3)))
            all_cities.add(_from)
            all_cities.add(_to)

        self.all_cities = frozenset(all_cities)

    def part1(self):
        queue: PriorityQueue[SearchAttempt] = PriorityQueue[SearchAttempt]()
        for city in self.all_cities:
            queue.push(SearchAttempt(0, city, frozenset({city})), 0)

        result = 0

        while not queue.empty:
            search: SearchAttempt = queue.pop()

            if search.visited == self.all_cities:
                result = search.distance
                break

            for edge in self.graph.edges_from(search.current):
                if edge.end in search.visited:
                    continue

                new_distance = search.distance + edge.weight
                new_visited = frozenset(search.visited.union({edge.end}))
                new_search = SearchAttempt(new_distance, edge.end, new_visited)

                queue.push(new_search, new_distance)

        print("Part 1:", result)

    def part2(self):
        queue = Queue()
        for city in self.all_cities:
            queue.put(SearchAttempt(0, city, frozenset({city})))

        result = 0

        while not queue.empty():
            search: SearchAttempt = queue.get()

            if search.visited == self.all_cities:
                result = max(search.distance, result)

            for edge in self.graph.edges_from(search.current):
                if edge.end in search.visited:
                    continue

                new_distance = search.distance + edge.weight
                new_visited = frozenset(search.visited.union({edge.end}))
                new_search = SearchAttempt(new_distance, edge.end, new_visited)

                queue.put(new_search)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D9("2015/9.txt")
    code.part1()
    code.part2()
