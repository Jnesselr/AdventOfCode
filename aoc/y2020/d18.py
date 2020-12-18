from enum import Enum
from typing import List, Union, NewType

from aoc.util.inputs import Input

Expression = NewType('Expression', List[Union[int, str]])


class PrecedenceRules(Enum):
    LEFT_TO_RIGHT = 0
    PLUS_IS_MIGHTY = 1

    def next_index(self, expression: Expression) -> int:
        if self == PrecedenceRules.PLUS_IS_MIGHTY:
            if '+' in expression:
                return expression.index('+')
        return 1  # Left to right makes this the next operator. Or we've wiped out all the + operators


class Y2020D18(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.expressions: List[Expression] = [
            Expression([
                int(x) if x.isnumeric() else str(x)
                for x in list(line.replace(' ', ''))
            ])
            for line in lines
        ]

    def part1(self):
        result = sum([self._evaluate(x, PrecedenceRules.LEFT_TO_RIGHT) for x in self.expressions])

        print("Part 1:", result)

    def part2(self):
        result = sum([self._evaluate(x, PrecedenceRules.PLUS_IS_MIGHTY) for x in self.expressions])

        print("Part 2:", result)

    @classmethod
    def _get_subexpression(cls, expression, starting_index):
        index = starting_index + 1
        parenthesis_count = 1
        while parenthesis_count > 0:
            if expression[index] == '(':
                parenthesis_count += 1
            elif expression[index] == ')':
                parenthesis_count -= 1
            index += 1
        return expression[starting_index + 1:index - 1]

    def _evaluate(self, expression: Expression, precedence: PrecedenceRules) -> int:
        result = expression.copy()

        while len(result) > 1:
            if '(' in result:  # We need to wipe out parenthesis first
                first_parenthesis = result.index('(')
                subexpression = self._get_subexpression(result, first_parenthesis)
                sub_value = self._evaluate(subexpression, precedence)
                result = result[0:first_parenthesis] + [sub_value] + \
                         result[first_parenthesis + len(subexpression) + 2:]
                continue

            next_index = precedence.next_index(result)
            next_operator = result[next_index]
            if next_operator == '*':
                f = int.__mul__
            elif next_operator == '+':
                f = int.__add__
            else:
                raise ValueError(f"Unknown operator {next_operator}")

            math_result = f(result[next_index - 1], result[next_index + 1])
            result = result[:next_index - 1] + [math_result] + result[next_index + 2:]

        return result[0]


if __name__ == '__main__':
    code = Y2020D18("2020/18.txt")
    code.part1()
    code.part2()
