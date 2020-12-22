import re
from dataclasses import dataclass
from typing import List, Final, Optional


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


"""
    val c = registerState.get(arguments.a)
    val d = registerState.get(arguments.b)
    var result: BigInt = c / d
    if(result * d < c) {
      result = result + d
    }

    while(registerState.get(arguments.c) >= result) {
      result = result + d
    }

    registerState.updated(arguments.c, result).updated(4, result * d)
    """


# Custom command solely for day 19
@dataclass(frozen=True)
class Idvup(Instruction):
    a: int
    b: int
    c: int
    opcode: Final[int] = 8

    def __call__(self, registers: List[int]) -> List[int]:
        registers = registers.copy()
        c = registers[self.a]
        d = registers[self.b]
        result = c // d
        if result * d < c:
            result = result + d

        while registers[self.c] >= result:
            result = result + d

        registers[self.c] = result
        registers[4] = result * d

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

    def __init__(self, instructions: List[str]):
        opcode_to_instruction_class = {}
        for cls in self.instruction_classes:
            opcode_to_instruction_class[cls.opcode] = cls
            opcode_to_instruction_class[cls.__name__[1:]] = cls

        self.instructions: List[Instruction] = []
        self.ip_register: Optional[int] = None
        self.registers = [0] * 6

        for instruction in instructions:
            if instruction[0] == '#':
                matched = re.match(r'#ip (\d+)', instruction)
                self.ip_register = int(matched.group(1))
                continue

            instruction = [
                int(x) if x.isnumeric() else x for x in instruction.split(' ')
            ]

            opcode = instruction[0]
            cls = opcode_to_instruction_class[opcode]
            a = instruction[1]
            b = instruction[2]
            c = instruction[3]

            self.instructions.append(cls(a, b, c))

    def reset(self):
        for i in range(len(self.registers)):
            self.registers[i] = 0

    def run(self):
        ip = 0
        while True:
            instruction = self.instructions[ip]

            if self.ip_register is not None:
                self.registers[self.ip_register] = ip

            self.registers = instruction(self.registers)

            if self.ip_register is not None:
                ip = self.registers[self.ip_register]

            ip += 1

            if ip >= len(self.instructions):
                break
