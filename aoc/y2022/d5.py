import re
from dataclasses import dataclass
from typing import Dict, List

from aoc.util.inputs import Input

@dataclass
class Instruction:
    count: int
    f: int
    t: int


class Y2022D5(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        space_row_index = lines.index('')
        column_num_row = lines[space_row_index-1]
        self.stacks: Dict[int, List[str]] = {}

        for char_index, char in enumerate(column_num_row):
            if char == ' ':
                continue

            result = []

            for row_index in range(space_row_index-2, -1, -1):
                line = lines[row_index]
                if char_index >= len(line) or line[char_index] == ' ':
                    break
                result.append(line[char_index])

            self.stacks[int(char)] = result

        self.instructions = []

        regex = re.compile(r'move (\d+) from (\d+) to (\d+)')
        for line in lines[space_row_index+1:]:
            match = regex.match(line)
            self.instructions.append(Instruction(
                count=int(match.group(1)),
                f=int(match.group(2)),
                t=int(match.group(3))
            ))

    def _copy(self):
        result = {}

        for key, value in self.stacks.items():
            result[key] = list(value)

        return result

    def part1(self):
        my_stacks = self._copy()
        for instruction in self.instructions:
            for _ in range(instruction.count):
                char = my_stacks[instruction.f].pop()
                my_stacks[instruction.t].append(char)

        result = ''.join([stack[-1] for stack in my_stacks.values()])

        print("Part 1:", result)

    def part2(self):
        my_stacks = self._copy()

        for instruction in self.instructions:
            my_list = []
            for _ in range(instruction.count):
                char = my_stacks[instruction.f].pop()
                my_list.insert(0, char)
            my_stacks[instruction.t].extend(my_list)

        result = ''.join([stack[-1] for stack in my_stacks.values()])

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D5("2022/5.txt")
    code.part1()
    code.part2()
