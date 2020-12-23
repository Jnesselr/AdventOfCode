from aoc.util.inputs import Input
from aoc.y2018.watch import WatchVM, Ieqrr


class FakeVM(object):
    def __init__(self):
        self.registers = [0] * 6
        self._breakpoint = None

    def reset(self):
        self.registers = [0] * 6
        self._breakpoint = None

    def set_breakpoint(self, _breakpoint):
        self._breakpoint = _breakpoint

    def run(self):
        self.registers[2] = 65536
        self.registers[5] = 7571367

        while True:
            self.registers[5] = (self.registers[5] + (self.registers[2] & 255))
            self.registers[5] = ((self.registers[5] & 16777215) * 65899) & 16777215

            if 256 > self.registers[2]:
                if not self._breakpoint(self):
                    return

                if self.registers[5] == self.registers[0]:
                    break

                self.registers[2] = self.registers[5] | 65536
                self.registers[5] = 7571367
                continue

            self.registers[2] = self.registers[2] // 256


class Y2018D21(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        # Using our watch vm will eventually finish, but it takes hours.
        # Using our Fake VM, created based on my input specifically, finishes instantly.
        self._use_watch_vm = False

        if self._use_watch_vm:
            self.vm = WatchVM(lines)
        else:
            self.vm = FakeVM()

    def part1(self):
        self.vm.reset()
        result = 0

        def _breakpoint(vm):
            nonlocal result
            result = vm.registers[5]
            return False  # Don't continue executing

        self._setup_breakpoint(_breakpoint)
        self.vm.run()

        print("Part 1:", result)

    def part2(self):
        self.vm.reset()
        seen = set()
        result = 0

        # Try to find the last value before the next value would cause it to loop
        def _breakpoint(vm):
            nonlocal result
            register_value = vm.registers[5]

            if register_value in seen:
                return False

            seen.add(register_value)
            result = register_value
            return True

        self._setup_breakpoint(_breakpoint)
        self.vm.run()

        print("Part 2:", result)

    def _setup_breakpoint(self, _breakpoint):
        if isinstance(self.vm, WatchVM):
            breakpoint_indexes = [
                index for index, instruction in enumerate(self.vm.instructions)
                if isinstance(instruction, Ieqrr) and \
                   (instruction.a == 0 or instruction.b == 0)
            ]

            if len(breakpoint_indexes) != 1:
                raise ValueError("Expected one breakpoint location!")

            self.vm.breakpoint(breakpoint_indexes[0], _breakpoint)
        else:
            self.vm.set_breakpoint(_breakpoint)


if __name__ == '__main__':
    code = Y2018D21("2018/21.txt")
    code.part1()
    code.part2()
