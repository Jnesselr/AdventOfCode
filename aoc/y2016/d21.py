import re
from typing import List, Union

from aoc.util.inputs import Input


class Scrambler(object):
    swap_position = re.compile(r'swap position (\d) with position (\d)')
    swap_letter = re.compile(r'swap letter (\w) with letter (\w)')
    reverse_positions = re.compile(r'reverse positions (\d) through (\d)')
    rotate = re.compile(r'rotate (left|right) (\d) step')
    move_position = re.compile(r'move position (\d) to position (\d)')
    rotate_position = re.compile(r'rotate based on position of letter (\w)')

    def __init__(self, password):
        self.password_length = len(password)
        self.letter_to_index = {}
        self.index_to_letter = {}

        for index, letter in enumerate(password):
            self.letter_to_index[letter] = index
            self.index_to_letter[index] = letter

    @property
    def password(self):
        return "".join([y for _, y in sorted(self.index_to_letter.items())])

    def scramble(self, operations: List[str]):
        for operation in operations:
            if (matched := self.swap_position.match(operation)) is not None:
                x_position = int(matched.group(1))
                y_position = int(matched.group(2))
                self._swap(x_position, y_position)
            elif (matched := self.swap_letter.match(operation)) is not None:
                x_letter = matched.group(1)
                y_letter = matched.group(2)
                self._swap(x_letter, y_letter)
            elif (matched := self.reverse_positions.match(operation)) is not None:
                start_position = int(matched.group(1))
                end_position = int(matched.group(2))
                self._reverse(start_position, end_position)
            elif (matched := self.rotate.match(operation)) is not None:
                left_or_right = matched.group(1)
                step_count = int(matched.group(2))

                if left_or_right == "left":
                    step_count = -step_count

                self._rotate_right(step_count)
            elif (matched := self.move_position.match(operation)) is not None:
                start_position = int(matched.group(1))
                end_position = int(matched.group(2))
                self._move_position(start_position, end_position)
            elif (matched := self.rotate_position.match(operation)) is not None:
                letter = matched.group(1)
                index = self.letter_to_index[letter]
                rotate_count = 1
                if index >= 4:
                    rotate_count += 1

                rotate_count += index
                self._rotate_right(rotate_count)
            else:
                raise ValueError(f"Could not match: {operation}")

    def unscramble(self, operations: List[str]):
        operations = operations.copy()
        operations.reverse()

        for operation in operations:
            if (matched := self.swap_position.match(operation)) is not None:
                x_position = int(matched.group(1))
                y_position = int(matched.group(2))
                self._swap(x_position, y_position)
            elif (matched := self.swap_letter.match(operation)) is not None:
                x_letter = matched.group(1)
                y_letter = matched.group(2)
                self._swap(x_letter, y_letter)
            elif (matched := self.reverse_positions.match(operation)) is not None:
                start_position = int(matched.group(1))
                end_position = int(matched.group(2))
                self._reverse(start_position, end_position)
            elif (matched := self.rotate.match(operation)) is not None:
                left_or_right = matched.group(1)
                step_count = int(matched.group(2))

                if left_or_right == "right":
                    step_count = -step_count

                self._rotate_right(step_count)
            elif (matched := self.move_position.match(operation)) is not None:
                start_position = int(matched.group(1))
                end_position = int(matched.group(2))
                self._move_position(end_position, start_position)
            elif (matched := self.rotate_position.match(operation)) is not None:
                letter = matched.group(1)
                current_position = self.letter_to_index[letter]

                position_options = set()
                for i in range(self.password_length):
                    test_position = (1 + (1 if i >= 4 else 0) + 2 * i) % self.password_length
                    if test_position == current_position:
                        position_options.add(i)

                if len(position_options) == 1:
                    rotate_amount = (current_position - position_options.pop()) % self.password_length
                    self._rotate_right(-rotate_amount)
                else:
                    raise ValueError(f"Could not reverse '{operation}' on {self.password}. Options {position_options}")
            else:
                raise ValueError(f"Could not match: {operation}")

    def _swap(self, x: Union[int, str], y: Union[int, str]):
        if isinstance(x, int):
            x_position = x
            x_letter = self.index_to_letter[x_position]
        else:
            x_letter = x
            x_position = self.letter_to_index[x_letter]

        if isinstance(y, int):
            y_position = y
            y_letter = self.index_to_letter[y_position]
        else:
            y_letter = y
            y_position = self.letter_to_index[y_letter]

        self.index_to_letter[x_position] = y_letter
        self.index_to_letter[y_position] = x_letter
        self.letter_to_index[x_letter] = y_position
        self.letter_to_index[y_letter] = x_position

    def _reverse(self, start_position, end_position):
        length = abs(start_position - end_position)
        for i in range((length // 2) + 1):
            x = (start_position + i) % self.password_length
            y = (end_position - i) % self.password_length
            self._swap(x, y)

    def _rotate_right(self, count):
        for letter, index in self.letter_to_index.items():
            new_index = (index + count) % self.password_length
            self.letter_to_index[letter] = new_index
            self.index_to_letter[new_index] = letter

    def _move_position(self, start_position: int, end_position: int):
        length = abs(start_position - end_position)
        moving_letter = self.index_to_letter[start_position]
        diff = 1 if end_position > start_position else -1

        for i in range(length):
            if end_position < start_position:
                i = -i
            to_position = (start_position + i) % self.password_length
            from_position = (to_position + diff) % self.password_length
            letter = self.index_to_letter[from_position]
            self.index_to_letter[to_position] = letter
            self.letter_to_index[letter] = to_position

        self.letter_to_index[moving_letter] = end_position
        self.index_to_letter[end_position] = moving_letter


class Y2016D21(object):
    def __init__(self, file_name):
        self.operations = Input(file_name).lines()

    def part1(self):
        scrambler = Scrambler("abcdefgh")
        scrambler.scramble(self.operations)
        result = scrambler.password

        print("Part 1:", result)

    def part2(self):
        scrambler = Scrambler("fbgdceah")
        scrambler.unscramble(self.operations)
        result = scrambler.password

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D21("2016/21.txt")
    code.part1()
    code.part2()
