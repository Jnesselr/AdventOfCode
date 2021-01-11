from __future__ import annotations
import re
from typing import List, Union


class Instruction(object):
    # result is instruction pointer change
    def __call__(self, assembunny: Assembunny) -> None:
        pass

    @staticmethod
    def _register_offset(value: str):
        return ord(value) - ord('a')

    @classmethod
    def _register_or_value(cls, value: Union[int, str], registers: List[int]) -> int:
        if isinstance(value, str):
            return registers[cls._register_offset(value)]
        return value


class Copy(Instruction):
    def __init__(self, x: Union[int, str], y: str):
        self.x = x if isinstance(x, str) and x.isalpha() else int(x)
        self.y = y

    def __call__(self, assembunny: Assembunny) -> None:
        value = self._register_or_value(self.x, assembunny.registers)
        assembunny.registers[self._register_offset(self.y)] = value

        assembunny.instruction_pointer += 1

    def __str__(self):
        return f"{self.x} -> {self.y}"


class Increase(Instruction):
    def __init__(self, x: str):
        self.x = x

    def __call__(self, assembunny: Assembunny) -> None:
        assembunny.registers[self._register_offset(self.x)] += 1

        assembunny.instruction_pointer += 1

    def __str__(self):
        return f"{self.x}++"


class Decrease(Instruction):
    def __init__(self, x: str):
        self.x = x

    def __call__(self, assembunny: Assembunny) -> None:
        assembunny.registers[self._register_offset(self.x)] -= 1

        assembunny.instruction_pointer += 1

    def __str__(self):
        return f"{self.x}--"


class JumpNotZero(Instruction):
    def __init__(self, x: Union[int, str], y: Union[int, str]):
        self.x = x if isinstance(x, str) and x.isalpha() else int(x)
        self.y = y if isinstance(y, str) and y.isalpha() else int(y)

    def __call__(self, assembunny: Assembunny) -> None:
        x_value = self._register_or_value(self.x, assembunny.registers)
        y_value = self._register_or_value(self.y, assembunny.registers)

        if x_value == 0:
            assembunny.instruction_pointer += 1
        else:
            assembunny.instruction_pointer += y_value

    def __str__(self):
        return f"if {self.x} != 0 jump {self.y}"


class Skip(Instruction):
    def __call__(self, assembunny: Assembunny) -> None:
        assembunny.instruction_pointer += 1

    def __str__(self):
        return f"nop"


class Toggle(Instruction):
    def __init__(self, x: Union[int, str]):
        self.x = int(x) if x.isnumeric() else x

    def __call__(self, assembunny: Assembunny) -> None:
        value = self._register_or_value(self.x, assembunny.registers)

        instruction_location = assembunny.instruction_pointer + value

        assembunny.instruction_pointer += 1

        if instruction_location < 0 or instruction_location >= len(assembunny.instructions):
            return

        instruction_to_modify = assembunny.instructions[instruction_location]

        new_instruction = Skip()
        if instruction_to_modify.__class__ == Increase:
            new_instruction = Decrease(instruction_to_modify.x)
        elif instruction_to_modify.__class__ in [Decrease, Toggle]:
            new_instruction = Increase(instruction_to_modify.x)
        elif instruction_to_modify.__class__ == JumpNotZero:
            if isinstance(instruction_to_modify.y, str):
                new_instruction = Copy(instruction_to_modify.x, instruction_to_modify.y)
        elif instruction_to_modify.__class__ == Copy:
            new_instruction = JumpNotZero(instruction_to_modify.x, instruction_to_modify.y)

        assembunny.instructions[instruction_location] = new_instruction

    def __str__(self):
        return f"toggle {self.x}"


class Assembunny(object):
    def __init__(self, lines):
        self._lines = lines

        self.instructions = []
        self.instruction_pointer = 0
        self.registers = [0] * 4

        self.reset()

    def reset(self):
        self.instructions = []
        for line in self._lines:
            if (matched := re.match(r'cpy (-?\d+|\w+) (\w+)', line)) is not None:
                self.instructions.append(Copy(matched.group(1), matched.group(2)))
            elif (matched := re.match(r'inc (\w+)', line)) is not None:
                self.instructions.append(Increase(matched.group(1)))
            elif (matched := re.match(r'dec (\w+)', line)) is not None:
                self.instructions.append(Decrease(matched.group(1)))
            elif (matched := re.match(r'jnz (-?\d+|\w+) (-?\d+|\w+)', line)) is not None:
                self.instructions.append(JumpNotZero(matched.group(1), matched.group(2)))
            elif (matched := re.match(r'tgl (-?\d+|\w+)', line)) is not None:
                self.instructions.append(Toggle(matched.group(1)))
            else:
                raise ValueError(f"Could not parse: {line}")

        self.instruction_pointer = 0
        self.registers = [0] * 4

    def run(self):
        while True:
            if self.instruction_pointer < 0 or self.instruction_pointer >= len(self.instructions):
                break

            instruction: Instruction = self.instructions[self.instruction_pointer]

            instruction(self)

    def print(self):
        for i in range(len(self.instructions)):
            number = f'{i:2d}'
            caret = '>' if i == self.instruction_pointer else ':'
            instruction = str(self.instructions[i])
            print(f"{number}{caret} {instruction}")
