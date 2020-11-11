from aoc.util.inputs import Input


class Intcode(object):
    def __init__(self, file_name):
        line = Input(file_name).line()
        codes = line.split(',')

        self._flash = {}
        for index in range(len(codes)):
            self._flash[index] = int(codes[index])

        self.ram = {}
        self.instruction_pointer = 0
        self.halted = False

        self.reset()

    def reset(self):
        self.ram = self._flash.copy()

        self.instruction_pointer = 0
        self.halted = False

    def run(self):
        if self.halted:
            return

        while True:
            command = self.ram[self.instruction_pointer]

            if command == 1:
                first = self.ram.setdefault(self.ram[self.instruction_pointer + 1], 0)
                second = self.ram.setdefault(self.ram[self.instruction_pointer + 2], 0)
                self.ram[self.ram[self.instruction_pointer + 3]] = first + second
                self.instruction_pointer += 4
            elif command == 2:
                first = self.ram.setdefault(self.ram[self.instruction_pointer + 1], 0)
                second = self.ram.setdefault(self.ram[self.instruction_pointer + 2], 0)
                self.ram[self.instruction_pointer + 3] = first * second
                self.instruction_pointer += 4
            elif command == 99:
                self.halted = True
                return
            else:
                raise ValueError(f"Unknown command {command}")