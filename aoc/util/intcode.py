from dataclasses import dataclass
from typing import List

from aoc.util.inputs import Input


@dataclass(frozen=True)
class InstructionType(object):
    parameter_count: int
    last_parameter_is_pointer: bool


@dataclass(frozen=True)
class Instruction(object):
    opcode: int
    params: List[int]


class Intcode(object):
    _instruction_types = {
        1: InstructionType(3, True),
        2: InstructionType(3, True),
        3: InstructionType(1, True),
        4: InstructionType(1, False),
        5: InstructionType(2, False),
        6: InstructionType(2, False),
        7: InstructionType(3, True),
        8: InstructionType(3, True),
        9: InstructionType(1, False),
        99: InstructionType(0, False)
    }

    def __init__(self, file_name):
        line = Input(file_name).line()
        codes = line.split(',')

        self._flash = {}
        for index in range(len(codes)):
            self._flash[index] = int(codes[index])

        self.ram = {}
        self.instruction_pointer = 0
        self.halted = False
        self.waiting_for_input = False
        self._input_address = 0
        self.has_output = False
        self._output_value = 0
        self._relative_base = 0

        self.reset()

    def reset(self):
        self.ram = self._flash.copy()

        self.instruction_pointer = 0
        self.halted = False
        self.waiting_for_input = False
        self._input_address = 0
        self.has_output = False
        self._output_value = 0
        self._relative_base = 0

    def input(self, value):
        if not self.waiting_for_input:
            raise ValueError("Cannot give input, invalid state")

        self.ram[self._input_address] = value
        self._input_address = 0
        self.waiting_for_input = False

        self.run()

    def input_str(self, value: str):
        for character in value:
            self.input(ord(character))

    def output(self):
        if not self.has_output:
            raise ValueError("No output available!")

        result = self._output_value

        self.has_output = False
        self._output_value = 0
        self.run()

        return result

    def output_str(self):
        if not self.has_output:
            raise ValueError("No output available!")

        line = ""

        while self.has_output:
            output = self.output()
            if output < 127:
                line += chr(output)
            else:
                # This output wasn't an ascii character, so we probably shouldn't treat it like that.
                # Queue it up for the next output command.
                self.has_output = True
                self._output_value = output
                break
        return line

    def _fetch(self) -> Instruction:
        code = self.ram[self.instruction_pointer]
        opcode = code % 100
        code = code // 100

        instruction_type: InstructionType = self._instruction_types[opcode]

        params = []
        for i in range(1, instruction_type.parameter_count + 1):
            address = self.instruction_pointer + i
            value = self.ram.setdefault(address, 0)
            mode = code % 10
            code = code // 10

            if i == instruction_type.parameter_count and instruction_type.last_parameter_is_pointer:
                if mode == 2:
                    params.append(self._relative_base + value)
                else:
                    params.append(value)
            elif mode == 0:
                params.append(self.ram.setdefault(value, 0))
            elif mode == 1:
                params.append(value)
            elif mode == 2:
                params.append(self.ram.setdefault(self._relative_base + value, 0))
            else:
                raise ValueError(f"Unknown parameter mode: {mode}")

        return Instruction(opcode, params)

    def run(self):
        if self.halted:
            return

        if self.waiting_for_input:
            raise ValueError("Waiting for input, cannot run!")

        if self.has_output:
            raise ValueError("Has output, cannot run!")

        while True:
            instruction: Instruction = self._fetch()
            self.instruction_pointer += len(instruction.params) + 1

            if instruction.opcode == 1:
                self.ram[instruction.params[2]] = instruction.params[0] + instruction.params[1]
            elif instruction.opcode == 2:
                self.ram[instruction.params[2]] = instruction.params[0] * instruction.params[1]
            elif instruction.opcode == 3:
                self._input_address = instruction.params[0]
                self.waiting_for_input = True
                return
            elif instruction.opcode == 4:
                self._output_value = instruction.params[0]
                self.has_output = True
                return
            elif instruction.opcode == 5:
                if instruction.params[0] != 0:
                    self.instruction_pointer = instruction.params[1]
            elif instruction.opcode == 6:
                if instruction.params[0] == 0:
                    self.instruction_pointer = instruction.params[1]
            elif instruction.opcode == 7:
                self.ram[instruction.params[2]] = 1 if instruction.params[0] < instruction.params[1] else 0
            elif instruction.opcode == 8:
                self.ram[instruction.params[2]] = 1 if instruction.params[0] == instruction.params[1] else 0
            elif instruction.opcode == 9:
                self._relative_base += instruction.params[0]
            elif instruction.opcode == 99:
                self.halted = True
                return
            else:
                raise ValueError(f"Opcode {instruction.opcode} not implemented!")
