import re
from queue import Queue
from typing import Callable, Optional

import z3
from z3 import Solver, Int, BitVec, ULT

from aoc.util.inputs import Input

OutputCallback = Callable[[int], None]


class NormalComputer:
    def __init__(self, program: list[int], a: int, b: int, c: int):
        self._program = program
        self._register_a = a
        self._register_b = b
        self._register_c = c
        self._instruction_pointer = 0
        self._started = False

    def run(self):
        if self._started:
            raise Exception("This computer has already been run")

        self._started = True
        result = []

        while self._instruction_pointer < len(self._program):
            next_ip = self._instruction_pointer + 2

            opcode = self._program[self._instruction_pointer]
            operand = self._program[self._instruction_pointer + 1]

            if opcode == 0:  # adv
                self._register_a = self._register_a // pow(2, self._combo_operand(operand))
            elif opcode == 1:  # bxl
                self._register_b ^= operand
            elif opcode == 2:  # bst
                self._register_b = self._combo_operand(operand) % 8
            elif opcode == 3:  # jnz
                if self._register_a != 0:
                    next_ip = operand
            elif opcode == 4:  # bxc
                self._register_b ^= self._register_c
            elif opcode == 5:  # out
                result.append(self._combo_operand(operand) % 8)
            elif opcode == 6:  # bdv
                self._register_b = self._register_a // pow(2, self._combo_operand(operand))
            elif opcode == 7:  # cdv
                self._register_c = self._register_a // pow(2, self._combo_operand(operand))

            self._instruction_pointer = next_ip

        return result

    def _combo_operand(self, operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return self._register_a
        if operand == 5:
            return self._register_b
        if operand == 6:
            return self._register_c
        if operand == 7:
            raise Exception("Reserved combo operand")


class Z3Computer:
    _bit_length = 64

    def __init__(self, program: list[int], b: int, c: int, max_a: Optional[int] = None):
        self._solver = Solver()
        self._program = program
        self._initial_a: BitVec = BitVec("a", self._bit_length)
        self._register_a: BitVec = self._initial_a
        self._register_b: BitVec = BitVec("b", self._bit_length)
        self._register_c: BitVec = BitVec("c", self._bit_length)
        self._outputs = {}
        for i, value in enumerate(program):
            out_int = BitVec(f"out_{i}", self._bit_length)
            self._outputs[i] = out_int
            self._solver.add(out_int == value)

        if max_a is not None:
            self._solver.add(ULT(self._register_a, max_a))
        self._solver.add(self._register_b == b)
        self._solver.add(self._register_c == c)

    def run(self) -> Optional[int]:
        for iteration_count in range(len(self._program)):
            for instruction_pointer in range(0, len(self._program), 2):
                opcode = self._program[instruction_pointer]
                operand = self._program[instruction_pointer + 1]

                if opcode == 0:  # adv
                    self._register_a = self._register_a / (1 << self._combo_operand(operand))
                elif opcode == 1:  # bxl
                    self._register_b ^= operand
                elif opcode == 2:  # bst
                    self._register_b = self._combo_operand(operand) % 8
                elif opcode == 3:  # jnz
                    continue  # We assume this is at the end of our program
                elif opcode == 4:  # bxc
                    self._register_b ^= self._register_c
                elif opcode == 5:  # out
                    self._solver.add(self._outputs[iteration_count] == self._combo_operand(operand) % 8)
                elif opcode == 6:  # bdv
                    self._register_b = self._register_a / (1 << self._combo_operand(operand))
                elif opcode == 7:  # cdv
                    self._register_c = self._register_a / (1 << self._combo_operand(operand))

        self._solver.add(self._register_a == 0)  # Must end with a being zero for the program to exit
        if self._solver.check() == z3.unsat:
            return None
        return self._solver.model()[self._initial_a].as_long()

    def _combo_operand(self, operand: int) -> Int:
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return self._register_a
        if operand == 5:
            return self._register_b
        if operand == 6:
            return self._register_c
        if operand == 7:
            raise Exception("Reserved combo operand")


class Y2024D17(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        register_re = re.compile(r'Register ([ABC]): (\d+)')
        program_re = re.compile(r'Program: ([\d,]+)')
        registers = {}
        self._program = []
        for line in lines:
            if line == "":
                continue

            if (match := register_re.match(line)) is not None:
                registers[match.group(1)] = int(match.group(2))

            if (match := program_re.match(line)) is not None:
                self._program = [int(x) for x in match.group(1).split(",")]

        self._register_a = registers['A']
        self._register_b = registers['B']
        self._register_c = registers['C']

    def part1(self):
        computer = NormalComputer(
            self._program,
            self._register_a,
            self._register_b,
            self._register_c
        )

        result = ",".join(str(x) for x in computer.run())

        print("Part 1:", result)

    def part2(self):
        max_a = None

        # We do this loop because the optimizer takes way longer than the normal solver here, but the normal solver
        # won't give us the smallest value. The compromise is to solve it by trying to decrease "a" until it is no
        # longer solvable.
        while True:
            z3_computer = Z3Computer(self._program, self._register_b, self._register_c, max_a=max_a)
            run_result = z3_computer.run()
            if run_result is None:
                result = max_a
                break
            else:
                max_a = run_result  # New max_a!

        print("Part 2:", result)

    def part2_not_z3(self):
        result = 0
        q = Queue()
        q.put(0)

        while not q.empty():
            a = q.get()

            a_options = [(a << 3) + i for i in range(8)]
            for option in a_options:
                computer = NormalComputer(self._program, option, self._register_b, self._register_c)
                output = computer.run()
                correct_a = self._program == output
                if correct_a:
                    result = option
                    q = Queue()  # Nothing more to process
                    break

                good_candidate = self._program[-len(output):] == output
                if good_candidate:
                    q.put(option)

        print("Part 2 [not z3]:", result)


if __name__ == '__main__':
    code = Y2024D17("2024/17.txt")
    code.part1()
    code.part2()
    code.part2_not_z3()
