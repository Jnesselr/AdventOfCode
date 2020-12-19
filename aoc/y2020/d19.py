import re

from aoc.util.inputs import Input


class Y2020D19(object):
    def __init__(self, file_name):
        rule_lines, self.messages = Input(file_name).grouped()

        self.rules = {}

        for line in rule_lines:
            key, value = line.split(': ')
            self.rules[int(key)] = value

    # Convert To Regex
    def _c2r(self, rule_value, depth, is_part_two) -> str:
        result = ""

        if '|' in rule_value:
            left, right = rule_value.split(' | ')
            left = self._c2r(left, depth + 1, is_part_two)
            right = self._c2r(right, depth + 1, is_part_two)
            result += f"({left}|{right})"
        elif '"' in rule_value:
            return rule_value[1]
        else:
            values = [int(x) for x in rule_value.split(' ')]
            for value in values:
                next_rule_value = self.rules[value]
                if value == 11 and is_part_two:
                    if depth > 6:  # Determined via empirical testing
                        return ''
                    else:
                        next_rule_value = '42 31 | 42 11 31'
                result += self._c2r(next_rule_value, depth + 1, is_part_two)
                if value == 8 and is_part_two:
                    result += '+'

        return result

    def part1(self):
        regex = f'^{self._c2r(self.rules[0], 0, False)}$'
        result = sum(1 for message in self.messages if re.match(regex, message) is not None)

        print("Part 1:", result)

    def part2(self):
        regex = f'^{self._c2r(self.rules[0], 0, True)}$'
        result = sum(1 for message in self.messages if re.match(regex, message) is not None)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D19("2020/19.txt")
    code.part1()
    code.part2()
