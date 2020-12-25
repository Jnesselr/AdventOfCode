from queue import Queue
from typing import Set

from aoc.util.graph import Graph
from aoc.util.inputs import Input


class Y2017D12(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.graph: Graph[int] = Graph[int]()
        self.all_nodes = set()

        for line in lines:
            door, programs = line.split(' <-> ')
            self.all_nodes.add(int(door))
            for program in programs.split(', '):
                self.all_nodes.add(int(program))
                self.graph.add(int(door), int(program))

    def part1(self):
        result = len(self._get_group_containing(0))

        print("Part 1:", result)

    def part2(self):
        groups = []
        remaining_nodes = self.all_nodes.copy()

        while len(remaining_nodes) > 0:
            program = remaining_nodes.pop()
            program_group = self._get_group_containing(program)
            groups.append(program_group)
            remaining_nodes -= program_group

        result = len(groups)

        print("Part 2:", result)

    def _get_group_containing(self, program) -> Set[int]:
        node_set: Set[int] = set()
        node_set.add(program)
        queue: Queue = Queue()
        queue.put(program)

        while not queue.empty():
            item = queue.get()

            for node in self.graph.nodes_from(item):
                if node not in node_set:
                    queue.put(node)
                    node_set.add(node)

        return node_set


if __name__ == '__main__':
    code = Y2017D12("2017/12.txt")
    code.part1()
    code.part2()
