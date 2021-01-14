import re
from aoc.util.graph import Graph
from aoc.util.inputs import Input


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
        result = self.graph.tsp()

        print("Part 1:", result)

    def part2(self):
        result = self.graph.highest_tsp()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D9("2015/9.txt")
    code.part1()
    code.part2()
