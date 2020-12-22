from dataclasses import dataclass
from typing import List

from aoc.util.inputs import Input
from aoc.util.possibility_reducer import reduce_possibilities
from aoc.y2018.watch import Instruction, WatchVM


@dataclass
class RegisterChange(object):
    before: List[int]
    command: List[int]
    after: List[int]


class Y2018D16(object):

    def __init__(self, file_name):
        groups = Input(file_name).grouped()
        self.program_code = groups[-1]
        self.register_changes = []

        for group in groups[:-1]:
            before: List[int] = [int(x) for x in group[0][9:-1].split(', ')]
            command: List[int] = [int(x) for x in group[1].split(' ')]
            after: List[int] = [int(x) for x in group[2][9:-1].split(', ')]

            self.register_changes.append(RegisterChange(before, command, after))

        # self._map_out_instructions()

    def part1(self):
        result = 0

        for register_change in self.register_changes:
            number_of_matches = 0
            for cls in WatchVM.instruction_classes:
                a: int = register_change.command[1]
                b: int = register_change.command[2]
                c: int = register_change.command[3]
                instruction: Instruction = cls(a, b, c)
                if instruction(register_change.before) == register_change.after:
                    number_of_matches += 1
            if number_of_matches >= 3:
                result += 1

        print("Part 1:", result)

    def part2(self):
        vm = WatchVM(self.program_code)
        vm.run()
        result = vm.registers[0]

        print("Part 2:", result)

    # Used to map out opcodes -> instructions the first time.
    # After that, they were encoded in the instruction class, itself for day 19
    def _map_out_instructions(self):
        possibility_map = {}
        for register_change in self.register_changes:
            matched_instructions = set()
            for cls in WatchVM.instruction_classes:
                a: int = register_change.command[1]
                b: int = register_change.command[2]
                c: int = register_change.command[3]
                instruction: Instruction = cls(a, b, c)
                if instruction(register_change.before) == register_change.after:
                    matched_instructions.add(cls)

            opcode = register_change.command[0]
            if opcode not in possibility_map:
                possibility_map[opcode] = matched_instructions
            else:
                possibility_map[opcode] = possibility_map[opcode].intersection(matched_instructions)

        opcode_to_instruction = reduce_possibilities(possibility_map)

        for key in sorted(opcode_to_instruction.keys()):
            value = opcode_to_instruction[key]
            print(key, value.__name__)


if __name__ == '__main__':
    code = Y2018D16("2018/16.txt")
    code.part1()
    code.part2()
