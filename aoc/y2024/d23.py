from collections import defaultdict
from queue import Queue

from aoc.util.inputs import Input


class Y2024D23(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        connection_map: defaultdict[str, set[str]] = defaultdict(lambda: set())

        q = Queue()
        self._computer_networks: set[frozenset[str]] = set()

        for line in lines:
            a, b = line.split('-')

            set_a = frozenset({a})
            set_b = frozenset({b})

            if set_a not in self._computer_networks:
                q.put(set_a)
                self._computer_networks.add(set_a)

            if set_b not in self._computer_networks:
                q.put(set_b)
                self._computer_networks.add(set_b)

            connection_map[a].add(b)
            connection_map[b].add(a)

        while not q.empty():
            current_computers: frozenset[str] = q.get()
            other_options = set(connection_map.keys())

            for other_computer in current_computers:
                other_options = other_options.intersection(connection_map[other_computer])

            for option in other_options:
                new_computer_set = current_computers.union({option})
                if new_computer_set in self._computer_networks:
                    continue

                q.put(new_computer_set)
                self._computer_networks.add(new_computer_set)

    def part1(self):
        result = 0

        for networks in self._computer_networks:
            if len(networks) != 3:
                continue
            a, b, c = networks

            if a[0] == 't' or b[0] == 't' or c[0] == 't':
                result += 1

        print("Part 1:", result)

    def part2(self):
        network = max(self._computer_networks, key=lambda n: len(n))
        result = ",".join(sorted(list(network)))

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2024D23("2024/23.txt")
    code.part1()
    code.part2()
