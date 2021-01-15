import re

from aoc.util.inputs import Input


class FirstComputer(object):
    def __init__(self, lines):
        self.lines = lines
        self.instruction_pointer = 0
        self.registers = [0, 0]

    def reset(self):
        self.instruction_pointer = 0
        self.registers = [0, 0]

    def run(self):
        while True:
            if self.instruction_pointer < 0 or self.instruction_pointer >= len(self.lines):
                return

            line = self.lines[self.instruction_pointer]
            self.instruction_pointer += 1

            if matched := re.match(r'jio ([ab]), ([+-]\d+)', line):
                register = matched.group(1)
                offset = int(matched.group(2))

                if self[register] == 1:
                    self.instruction_pointer = self.instruction_pointer - 1 + offset
            elif matched := re.match(r'jie ([ab]), ([+-]\d+)', line):
                register = matched.group(1)
                offset = int(matched.group(2))

                if self[register] % 2 == 0:
                    self.instruction_pointer = self.instruction_pointer - 1 + offset
            elif matched := re.match(r'jmp ([+-]\d+)', line):
                offset = int(matched.group(1))
                self.instruction_pointer = self.instruction_pointer - 1 + offset
            elif matched := re.match(r'inc ([ab])', line):
                register = matched.group(1)
                self[register] += 1
            elif matched := re.match(r'tpl ([ab])', line):
                register = matched.group(1)
                self[register] *= 3
            elif matched := re.match(r'hlf ([ab])', line):
                register = matched.group(1)
                self[register] //= 2
            else:
                raise ValueError(f"Could not match {line}")

    def __getitem__(self, register):
        return self.registers[ord(register) - ord('a')]

    def __setitem__(self, register, value):
        self.registers[ord(register) - ord('a')] = value


class Y2015D23(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.computer = FirstComputer(lines)

    def part1(self):
        self.computer.reset()
        self.computer.run()
        result = self.computer.registers[1]

        print("Part 1:", result)

    def part2(self):
        self.computer.reset()
        self.computer['a'] = 1
        self.computer.run()
        result = self.computer.registers[1]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D23("2015/23.txt")
    code.part1()
    code.part2()
