from dataclasses import dataclass
from typing import List, Final


class Instruction(object):
    def __call__(self, registers: List[int]) -> List[int]:
        pass


@dataclass(frozen=True)
class Iaddr(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 10

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = registers[self.a] + registers[self.b]

        return registers


@dataclass(frozen=True)
class Iaddi(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 15

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = registers[self.a] + self.b

        return registers


@dataclass(frozen=True)
class Imulr(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 11

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = registers[self.a] * registers[self.b]

        return registers


@dataclass(frozen=True)
class Imuli(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 13

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = registers[self.a] * self.b

        return registers


@dataclass(frozen=True)
class Ibanr(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 14

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = registers[self.a] & registers[self.b]

        return registers


@dataclass(frozen=True)
class Ibani(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 12

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = registers[self.a] & self.b

        return registers


@dataclass(frozen=True)
class Iborr(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 9

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = registers[self.a] | registers[self.b]

        return registers


@dataclass(frozen=True)
class Ibori(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 2

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = registers[self.a] | self.b

        return registers


@dataclass(frozen=True)
class Isetr(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 1

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = registers[self.a]

        return registers


@dataclass(frozen=True)
class Iseti(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 6

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = self.a

        return registers


@dataclass(frozen=True)
class Igtir(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 0

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = 1 if self.a > registers[self.b] else 0

        return registers


@dataclass(frozen=True)
class Igtri(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 4

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = 1 if registers[self.a] > self.b else 0

        return registers


@dataclass(frozen=True)
class Igtrr(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 3

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = 1 if registers[self.a] > registers[self.b] else 0

        return registers


@dataclass(frozen=True)
class Ieqir(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 5

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = 1 if self.a == registers[self.b] else 0

        return registers


@dataclass(frozen=True)
class Ieqri(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 7

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = 1 if registers[self.a] == self.b else 0

        return registers


@dataclass(frozen=True)
class Ieqrr(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 8

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        registers[self.c] = 1 if registers[self.a] == registers[self.b] else 0

        return registers


class WatchVM(object):
    instruction_classes = [
        Iaddr, Iaddi,
        Imulr, Imuli,
        Ibanr, Ibani,
        Iborr, Ibori,
        Isetr, Iseti,
        Igtir, Igtri, Igtrr,
        Ieqir, Ieqri, Ieqrr,
    ]

    def __init__(self, instructions: List[List[int]]):
        opcode_to_instruction_class = {}
        for cls in self.instruction_classes:
            opcode_to_instruction_class[cls.opcode] = cls

        self.instructions: List[Instruction] = []

        for instruction in instructions:
            opcode = instruction[0]
            cls = opcode_to_instruction_class[opcode]
            a = instruction[1]
            b = instruction[2]
            c = instruction[3]

            self.instructions.append(cls(a, b, c))

        self.registers = [0, 0, 0, 0]

    def run(self):
        for instruction in self.instructions:
            self.registers = instruction(self.registers)
