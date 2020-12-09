import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from aoc.util.inputs import Input


class InstructionType(Enum):
    NOP = auto()
    ACC = auto()
    JMP = auto()


@dataclass
class Instruction(object):
    type: InstructionType
    argument: int


class Program(object):
    def __init__(self, instructions: List[Instruction]):
        self.instructions = instructions
        self.infinite_loop = False
        self.booted = False
        self.accumulator = 0
        self.instruction_pointer = 0

    def run(self):
        seen_instruction_index = set()

        while True:
            if self.instruction_pointer in seen_instruction_index:
                self.infinite_loop = True
                return

            if self.instruction_pointer >= len(self.instructions):
                self.booted = True
                return

            instruction: Instruction = self.instructions[self.instruction_pointer]
            seen_instruction_index.add(self.instruction_pointer)

            if instruction.type == InstructionType.NOP:
                self.instruction_pointer += 1
            elif instruction.type == InstructionType.ACC:
                self.accumulator += instruction.argument
                self.instruction_pointer += 1
            elif instruction.type == InstructionType.JMP:
                self.instruction_pointer += instruction.argument


class Y2020D8(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.instructions = []
        for line in lines:
            if matched := re.match(r"nop ([+-]\d+)", line):
                self.instructions.append(Instruction(InstructionType.NOP, int(matched.group(1))))
            elif matched := re.match(r"acc ([+-]\d+)", line):
                self.instructions.append(Instruction(InstructionType.ACC, int(matched.group(1))))
            elif matched := re.match(r"jmp ([+-]\d+)", line):
                self.instructions.append(Instruction(InstructionType.JMP, int(matched.group(1))))
            else:
                raise ValueError("Nothing matched!")

    def part1(self):
        program = Program(self.instructions)
        program.run()
        result = program.accumulator

        print("Part 1:", result)

    def part2(self):
        result = 0
        for instruction_pointer, instruction in enumerate(self.instructions):
            if instruction.type == InstructionType.ACC:
                continue  # No acc instructions were harmed in the corruption of this boot code.

            instructions_copy = self.instructions.copy()
            if instruction.type == InstructionType.NOP:
                instructions_copy[instruction_pointer] = Instruction(InstructionType.JMP, instruction.argument)
            elif instruction.type == InstructionType.JMP:
                instructions_copy[instruction_pointer] = Instruction(InstructionType.NOP, instruction.argument)

            program = Program(instructions_copy)
            program.run()
            if program.booted:
                result = program.accumulator
                break

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D8("2020/8.txt")
    code.part1()
    code.part2()
