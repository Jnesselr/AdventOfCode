import re
from typing import List, Union

import sympy

from aoc.util.inputs import Input


class Coprocessor(object):
    def __init__(self, program: List[str]):
        self.program = program
        self.registers = {}

        self.terminated = False
        self.mul_called = 0

    def run(self):
        ip = 0
        while not self.terminated:
            if ip < 0 or ip >= len(self.program):
                self.terminated = True
                break

            line = self.program[ip]
            ip += 1
            if (matched := re.match(r'set (\w+) (\w+|-?\d+)', line)) is not None:
                register = matched.group(1)
                value = matched.group(2)
                self[register] = value
            elif (matched := re.match(r'sub (\w+) (\w+|-?\d+)', line)) is not None:
                register = matched.group(1)
                value = matched.group(2)
                self[register] -= self[value]
            elif (matched := re.match(r'mul (\w+) (\w+|-?\d+)', line)) is not None:
                register = matched.group(1)
                value = matched.group(2)
                self[register] *= self[value]
                self.mul_called += 1
            elif (matched := re.match(r'jnz (\w+) (\w+|-?\d+)', line)) is not None:
                register = matched.group(1)
                value = matched.group(2)

                if self[register] != 0:
                    ip += self[value] - 1
            else:
                raise ValueError(f"Unmatched line: {line}")

    def __getitem__(self, item: str) -> int:
        if isinstance(item, int):
            return item

        try:
            return int(item)
        except ValueError:
            return self.registers.setdefault(item, 0)

    def __setitem__(self, key: str, value: Union[str, int]):
        self.registers[key] = self[value]


class Y2017D23(object):
    def __init__(self, file_name):
        program = Input(file_name).lines()
        self.coprocessor = Coprocessor(program)
        self.coprocessor.run()

    def part1(self):
        result = self.coprocessor.mul_called

        print("Part 1:", result)

    @staticmethod
    def part2():
        result = 0

        # The problem basically requires you to reverse engineer it.
        # The "is prime" part of the code is N^2 for every N in our range.
        for i in range(108_100, 125_101, 17):
            if not sympy.isprime(i):
                result += 1

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D23("2017/23.txt")
    code.part1()
    code.part2()
