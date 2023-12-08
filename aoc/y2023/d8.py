import math
import re
from collections import Counter

from aoc.util.inputs import Input


class Y2023D8(object):
    def __init__(self, file_name):
        instructions, network = Input(file_name).grouped()
        self.instructions = instructions[0]

        self.left = {}
        self.right = {}

        network_re = re.compile('(\w+) = \((\w+), (\w+)\)')
        for line in network:
            match = network_re.match(line)
            from_node = match.group(1)
            self.left[from_node] = match.group(2)
            self.right[from_node] = match.group(3)

    def part1(self):
        result = self._find_steps_required('AAA', lambda n: n == 'ZZZ')

        print("Part 1:", result)

    def part2(self):
        nodes_ending_with_a = [node for node in self.left.keys() if node[-1] == 'A']
        nodes_ending_with_z = set(node for node in self.left.keys() if node[-1] == 'Z')

        steps_taken = []
        for node in nodes_ending_with_a:
            steps = self._find_steps_required(node, lambda n: n in nodes_ending_with_z)
            steps_taken.append(steps)

        result = math.lcm(*steps_taken)

        print("Part 2:", result)

    def _find_steps_required(self, current_node, test):
        steps_taken = 0
        while True:
            for instruction in self.instructions:
                if instruction == 'L':
                    current_node = self.left[current_node]
                else:
                    current_node = self.right[current_node]

                steps_taken += 1

                if test(current_node):
                    return steps_taken


if __name__ == '__main__':
    code = Y2023D8("2023/8.txt")
    code.part1()
    code.part2()
