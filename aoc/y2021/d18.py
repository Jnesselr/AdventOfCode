import itertools
from dataclasses import dataclass, field
from typing import Union, List, Optional

from aoc.util.inputs import Input


@dataclass
class SnailFishNumber(object):
    left: Optional[Union[int, 'SnailFishNumber']] = field(default=None)
    right: Optional[Union[int, 'SnailFishNumber']] = field(default=None)
    parent: Optional['SnailFishNumber'] = field(default=None)

    @staticmethod
    def read(line: str) -> 'SnailFishNumber':
        stack: List[SnailFishNumber] = []

        to_store: Optional[Union[int, 'SnailFishNumber']] = None
        for index, value in enumerate(line):
            to_store = None
            if value == '[':
                stack.append(SnailFishNumber())
            elif value == ']':
                to_store = stack.pop()
            elif value == ',':
                continue
            else:
                to_store = int(value)

            if to_store is not None:
                if len(stack) == 0:
                    return to_store
                fish_num = stack[-1]
                if fish_num.left is None:
                    fish_num.left = to_store
                else:
                    fish_num.right = to_store

                if isinstance(to_store, SnailFishNumber):
                    to_store.parent = fish_num

        return to_store

    @property
    def magnitude(self) -> int:
        result = 0

        result += 3 * (self.left if isinstance(self.left, int) else self.left.magnitude)
        result += 2 * (self.right if isinstance(self.right, int) else self.right.magnitude)

        return result

    def __add__(self, other: 'SnailFishNumber') -> 'SnailFishNumber':
        result = SnailFishNumber.read(f'[{self},{other}]')
        result.reduce()

        return result

    def __str__(self):
        return f"[{self.left},{self.right}]"

    def reduce(self):
        anything_changed = True
        while anything_changed:
            # print(self)
            anything_changed = False

            # Try to explode
            if self._explode():
                anything_changed = True
                continue

            # Try to split
            if self._split(self):
                anything_changed = True
                continue

    def _explode(self) -> bool:
        def _get_first_exploding(
                number: SnailFishNumber,
                current_depth: int) -> Optional[SnailFishNumber]:
            if current_depth >= 4:
                return number

            if isinstance(number.left, SnailFishNumber):
                left_result = _get_first_exploding(number.left, current_depth + 1)
                if left_result is not None:
                    return left_result

            if isinstance(number.right, SnailFishNumber):
                right_result = _get_first_exploding(number.right, current_depth + 1)
                if right_result is not None:
                    return right_result

            return None

        first_exploding = _get_first_exploding(self, 0)
        if first_exploding is None:
            return False

        sub = first_exploding
        parent = sub.parent
        while parent is not None and parent.left is sub:
            sub = parent
            parent = sub.parent

        if parent is not None:
            def _add_to_right(
                    p: SnailFishNumber,
                    num_to_add: int
            ) -> bool:
                if isinstance(p.right, SnailFishNumber):
                    if _add_to_right(p.right, num_to_add):
                        return True
                else:
                    p.right += num_to_add
                    return True

                if isinstance(p.left, SnailFishNumber):
                    if _add_to_right(p.left, num_to_add):
                        return True
                else:
                    p.left += num_to_add
                    return True

                return False

            if isinstance(parent.left, SnailFishNumber):
                _add_to_right(parent.left, first_exploding.left)
            else:
                parent.left += first_exploding.left

        sub = first_exploding
        parent = sub.parent
        while parent is not None and parent.right is sub:
            sub = parent
            parent = sub.parent

        if parent is not None:
            def _add_to_left(
                    p: SnailFishNumber,
                    num_to_add: int
            ) -> bool:
                if isinstance(p.left, int):
                    p.left += num_to_add
                    return True
                elif isinstance(p.left, SnailFishNumber):
                    if _add_to_left(p.left, num_to_add):
                        return True

                if isinstance(p.right, int):
                    p.right += num_to_add
                    return True
                elif isinstance(p.right, SnailFishNumber):
                    if _add_to_left(p.right, num_to_add):
                        return True

                return False

            if isinstance(parent.right, SnailFishNumber):
                _add_to_left(parent.right, first_exploding.right)
            else:
                parent.right += first_exploding.right

        if first_exploding.parent.left is first_exploding:
            first_exploding.parent.left = 0
        elif first_exploding.parent.right is first_exploding:
            first_exploding.parent.right = 0

        return True

    @classmethod
    def _split(cls, number: 'SnailFishNumber') -> bool:
        def _get_pair(value: int) -> SnailFishNumber:
            return SnailFishNumber(
                left=value // 2,
                right=(value + 1) // 2,
                parent=number
            )

        if isinstance(number.left, SnailFishNumber):
            if cls._split(number.left):
                return True
        elif number.left > 9:
            number.left = _get_pair(number.left)
            return True
        if isinstance(number.right, SnailFishNumber):
            if cls._split(number.right):
                return True
        elif number.right > 9:
            number.right = _get_pair(number.right)
            return True

        return False


class Y2021D18(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self._fish_nums: List[SnailFishNumber] = [SnailFishNumber.read(l) for l in lines]

    def part1(self):
        number = self._fish_nums[0]

        for next_num in self._fish_nums[1:]:
            number = number + next_num

        result = number.magnitude

        print("Part 1:", result)

    def part2(self):
        result = 0
        left: SnailFishNumber
        right: SnailFishNumber
        for left, right in itertools.product(self._fish_nums, repeat=2):
            if left is right:
                continue
            s = (left + right)
            magnitude = s.magnitude
            # print(left, right, s, magnitude)
            result = max(result, magnitude)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D18("2021/18.txt")
    code.part1()
    code.part2()
