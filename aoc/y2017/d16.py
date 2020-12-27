from typing import Dict, List

from aoc.util import alphabet
from aoc.util.inputs import Input


class ProgramDance(object):
    def __init__(self, dance_moves: List[str]):
        self.dance_moves = dance_moves

        self.program_count = 16
        self.program_to_index: Dict[str, int] = {}
        self.index_to_program: Dict[int, str] = {}

        self.reset()

    def reset(self):
        for index in range(self.program_count):
            program = alphabet[index]
            self.program_to_index[program] = index
            self.index_to_program[index] = program

    @property
    def programs(self):
        return "".join(self.index_to_program[index] for index in range(self.program_count))

    def dance(self):
        for move in self.dance_moves:
            if move[0] == 's':
                self.spin(int(move[1:]))
            elif move[0] == 'x':
                left, right = move[1:].split('/')
                self.exchange(int(left), int(right))
            elif move[0] == 'p':
                left, right = move[1:].split('/')
                self.partner(left, right)
            else:
                raise ValueError(f"Unknown move {move}")

    def spin(self, times: int):
        for i in range(self.program_count):
            program = alphabet[i]
            new_index = (self.program_to_index[program] + times) % self.program_count
            self.program_to_index[program] = new_index
            self.index_to_program[new_index] = program

    def exchange(self, index_a: int, index_b: int):
        program_a = self.index_to_program[index_a]
        program_b = self.index_to_program[index_b]

        self.index_to_program[index_a] = program_b
        self.index_to_program[index_b] = program_a
        self.program_to_index[program_a] = index_b
        self.program_to_index[program_b] = index_a

    def partner(self, program_a: str, program_b: str):
        index_a = self.program_to_index[program_a]
        index_b = self.program_to_index[program_b]

        self.index_to_program[index_a] = program_b
        self.index_to_program[index_b] = program_a
        self.program_to_index[program_a] = index_b
        self.program_to_index[program_b] = index_a


class Y2017D16(object):
    def __init__(self, file_name):
        line = Input(file_name).line()

        dance_moves = line.split(',')
        self.dance = ProgramDance(dance_moves)

    def part1(self):
        self.dance.reset()
        self.dance.dance()

        result = self.dance.programs

        print("Part 1:", result)

    def part2(self):
        self.dance.reset()
        seen: Dict[str, int] = {}

        i = 0
        loops_needed = 1000000000
        for i in range(loops_needed):
            program_string = self.dance.programs

            if program_string in seen:
                break

            seen[program_string] = i
            self.dance.dance()

        original_instance = seen[self.dance.programs]
        loop_size = i - original_instance
        needed_index = (loops_needed - original_instance) % loop_size
        result = [key for key, value in seen.items() if value == needed_index].pop()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D16("2017/16.txt")
    code.part1()
    code.part2()
