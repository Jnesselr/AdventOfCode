import re
from typing import Dict

from aoc.util.graph import Graph
from aoc.util.inputs import Input


class Y2017D7(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.disk_weights: Dict[str, int] = {}
        self.graph: Graph[str] = Graph[str](directional=True)

        for line in lines:
            matched = re.match(r'(\w+) \((\d+)\)( -> .*)?', line)
            name = matched.group(1)
            weight = int(matched.group(2))

            self.disk_weights[name] = weight

            holding_disks = matched.group(3)
            if holding_disks is not None:
                disks = holding_disks[4:].split(', ')
                for disk in disks:
                    self.graph.add(name, disk)

        self.root_node = list(self.disk_weights.keys())[0]
        while len(parent_nodes := self.graph.nodes_to(self.root_node)) > 0:
            self.root_node = list(parent_nodes)[0]

    def part1(self):
        result = self.root_node

        print("Part 1:", result)

    def part2(self):
        result = 0
        total_weights = {}

        def _get_total_weight(node: str) -> int:
            nonlocal result
            if node in total_weights:
                return total_weights[node]

            sub_nodes = self.graph.nodes_from(node)
            weights = dict((x, _get_total_weight(x)) for x in sub_nodes)

            values_set = set(weights.values())
            if len(values_set) > 1 and result == 0:
                by_value = {}

                for key, value in weights.items():
                    by_value.setdefault(value, set()).add(key)

                correct_value = None
                incorrect_value = None
                incorrect_node = None

                for key in by_value.keys():
                    if len(by_value[key]) == 1:
                        incorrect_value = key
                        incorrect_node = list(by_value[key])[0]
                    else:
                        correct_value = key

                result = self.disk_weights[incorrect_node] + (correct_value - incorrect_value)

            total_weights[node] = self.disk_weights[node] + sum(weights.values())

            return total_weights[node]

        _get_total_weight(self.root_node)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D7("2017/7.txt")
    code.part1()
    code.part2()
