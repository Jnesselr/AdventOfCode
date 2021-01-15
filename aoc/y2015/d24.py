from functools import reduce
from itertools import combinations

from aoc.util.inputs import Input


class Y2015D24(object):
    def __init__(self, file_name):
        self.packages = Input(file_name).ints()

    def part1(self):
        group_weight = sum(self.packages) // 3

        result = self._best_quantum_entanglement(group_weight)

        print("Part 1:", result)

    def part2(self):
        group_weight = sum(self.packages) // 4

        result = self._best_quantum_entanglement(group_weight)

        print("Part 2:", result)

    def _best_quantum_entanglement(self, group_weight):
        possible_passenger_compartment_groups = []

        length = 0
        while len(possible_passenger_compartment_groups) == 0:
            length += 1
            for combo in combinations(self.packages, r=length):
                if sum(combo) == group_weight:
                    possible_passenger_compartment_groups.append(combo)

        def quantum_entanglement(group):
            return reduce(lambda acc, cur: acc*cur, group)

        best_group = sorted(possible_passenger_compartment_groups, key=lambda c: quantum_entanglement(c))[0]

        return quantum_entanglement(best_group)


if __name__ == '__main__':
    code = Y2015D24("2015/24.txt")
    code.part1()
    code.part2()
