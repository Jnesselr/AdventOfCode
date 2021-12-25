import re
from typing import Dict

from z3 import Int, IntVal, ArithRef, If, Optimize, And

from aoc.util.inputs import Input


class Y2021D24(object):
    _re_inp = re.compile(r'inp ([wxyz])')
    _re_add = re.compile(r'add ([wxyz]) ([wxyz]|-?\d+)')
    _re_mul = re.compile(r'mul ([wxyz]) ([wxyz]|-?\d+)')
    _re_div = re.compile(r'div ([wxyz]) ([wxyz]|-?\d+)')
    _re_mod = re.compile(r'mod ([wxyz]) ([wxyz]|-?\d+)')
    _re_eql = re.compile(r'eql ([wxyz]) ([wxyz]|-?\d+)')

    def __init__(self, file_name):
        self.solver = Optimize()

        inputs = [Int(f'model_{i}') for i in range(14)]
        self.solver.add([i >= 1 for i in inputs])
        self.solver.add([i <= 9 for i in inputs])

        # Please don't ask me to explain this. There's a common pattern in the input code that treats z like a number
        # of base 26 and the operations are either right shift or left shift on that number +- some value.
        self.solver.add(inputs[0] + 6 - 6 == inputs[13])
        self.solver.add(inputs[1] + 11 - 6 == inputs[12])
        self.solver.add(inputs[2] + 5 - 13 == inputs[11])
        self.solver.add(inputs[3] + 6 - 8 == inputs[8])
        self.solver.add(inputs[4] + 8 - 1 == inputs[5])
        self.solver.add(inputs[6] + 9 - 16 == inputs[7])
        self.solver.add(inputs[9] + 13 - 16 == inputs[10])

        my_sum = IntVal(0)
        for index in range(len(inputs)):
            my_sum = (my_sum * 10) + inputs[index]

        self.value = Int('value')
        self.solver.add(my_sum == self.value)

    def part1(self):
        self.solver.push()

        self.solver.maximize(self.value)
        self.solver.check()
        result = self.solver.model()[self.value]

        self.solver.pop()

        print("Part 1:", result)

    def part2(self):
        self.solver.push()
        
        self.solver.minimize(self.value)
        self.solver.check()
        result = self.solver.model()[self.value]

        self.solver.pop()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D24("2021/24.txt")
    code.part1()
    code.part2()
