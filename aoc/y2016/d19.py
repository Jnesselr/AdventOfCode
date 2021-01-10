from collections import deque

from aoc.util.inputs import Input


class Y2016D19(object):
    def __init__(self, file_name):
        self.num_elves = Input(file_name).int()

    def part1(self):
        # This is the Josephus problem
        highest_power_of_two = 1
        while highest_power_of_two * 2 < self.num_elves:
            highest_power_of_two *= 2

        diff = self.num_elves - highest_power_of_two
        result = 2 * diff + 1

        print("Part 1:", result)

    def part2(self):
        """
        Instead of one big list, we treat this as two lists. The elf on the end of the bigger list
        gets stolen from. Then we essentially move the elves around so our "opposite side of the
        circle" constraint is still valid with our two queues.
        """

        left = deque(i for i in range(1, (self.num_elves // 2) + 1))
        right = deque(i for i in range(self.num_elves, self.num_elves // 2, -1))

        while left and right:
            if len(left) > len(right):
                left.pop()
            else:
                right.popleft()

            # rotate
            right.append(left.popleft())
            left.append(right.popleft())

        result = left[0] or right[0]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D19("2016/19.txt")
    code.part1()
    code.part2()
