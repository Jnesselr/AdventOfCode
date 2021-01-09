import re
from typing import List, Union


class Instruction(object):
    # result is instruction pointer change
    def __call__(self, registers: List[int]) -> int:
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
        self.x = int(x) if x.isnumeric() else x
        self.y = y

    def __call__(self, registers: List[int]) -> int:
        value = self._register_or_value(self.x, registers)
        registers[self._register_offset(self.y)] = value

        return 1


class Increase(Instruction):
    def __init__(self, register: str):
        self.register = register

    def __call__(self, registers: List[int]) -> int:
        registers[self._register_offset(self.register)] += 1

        return 1


class Decrease(Instruction):
    def __init__(self, register: str):
        self.register = register

    def __call__(self, registers: List[int]) -> int:
        registers[self._register_offset(self.register)] -= 1

        return 1


class JumpNotZero(Instruction):
    def __init__(self, x: Union[int, str], y: int):
        self.x = int(x) if x.isnumeric() else x
        self.y = y

    def __call__(self, registers: List[int]) -> int:
        value = self._register_or_value(self.x, registers)

        if value == 0:
            return 1
        else:
            return self.y


class Assembunny(object):
    def __init__(self, lines):
        self.instructions = []
        for line in lines:
            if (matched := re.match(r'cpy (-?\d+|\w+) (\w+)', line)) is not None:
                self.instructions.append(Copy(matched.group(1), matched.group(2)))
            elif (matched := re.match(r'inc (\w+)', line)) is not None:
                self.instructions.append(Increase(matched.group(1)))
            elif (matched := re.match(r'dec (\w+)', line)) is not None:
                self.instructions.append(Decrease(matched.group(1)))
            elif (matched := re.match(r'jnz (-?\d+|\w+) (-?\d+)', line)) is not None:
                self.instructions.append(JumpNotZero(matched.group(1), int(matched.group(2))))
            else:
                raise ValueError(f"Could not parse: {line}")

        self.instruction_pointer = 0
        self.registers = [0] * 4

    def reset(self):
        self.instruction_pointer = 0
        self.registers = [0] * 4

    def run(self):
        while True:
            if self.instruction_pointer < 0 or self.instruction_pointer >= len(self.instructions):
                break

            instruction: Instruction = self.instructions[self.instruction_pointer]

            self.instruction_pointer += instruction(self.registers)
