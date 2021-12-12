from dataclasses import field, dataclass
from queue import Queue
from typing import Set, Dict

from aoc.util.graph import Graph
from aoc.util.inputs import Input


@dataclass
class CavePath(object):
    current: str
    path: str
    seen: Dict[str, int] = field(default_factory=lambda: dict())

    def move(self, node: str) -> 'CavePath':
        new_seen = self.seen.copy()
        new_seen[node] = new_seen.setdefault(node, 0) + 1

        return CavePath(
            current=node,
            path=self.path + "," + node,
            seen=new_seen
        )


class Y2021D12(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self._graph: Graph[str] = Graph()

        for line in lines:
            start, end = line.split('-')
            self._graph.add(start, end)

    def part1(self):
        good_paths: Set[str] = set()

        start = CavePath("start", "start")
        queue = Queue()
        queue.put(start)

        while not queue.empty():
            item: CavePath = queue.get()

            possible_nodes = self._graph.nodes_from(item.current)

            for node in possible_nodes:
                if node.islower() and node in item.seen:
                    continue

                if node == "start":
                    continue  # Don't go back to the start

                next_node = item.move(node)
                if node == "end":
                    good_paths.add(next_node.path)
                else:
                    queue.put(next_node)

        result = len(good_paths)

        print("Part 1:", result)

    def part2(self):
        good_paths: Set[str] = set()

        start = CavePath("start", "start")
        queue = Queue()
        queue.put(start)

        while not queue.empty():
            # print(queue.qsize())
            item: CavePath = queue.get()

            possible_nodes = self._graph.nodes_from(item.current)

            for node in possible_nodes:
                if node.islower() and node in item.seen:
                    if item.seen[node] >= 2:
                        continue

                    if any([True for key, value in item.seen.items() if key.islower() and value == 2]):
                        continue

                if node == "start":
                    continue  # Don't go back to the start

                next_node = item.move(node)
                if node == "end":
                    good_paths.add(next_node.path)
                else:
                    queue.put(next_node)

        result = len(good_paths)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D12("2021/12.txt")
    code.part1()
    code.part2()
