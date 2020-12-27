from aoc.util.inputs import Input


class Y2017D17(object):
    def __init__(self, file_name):
        self.step_count = Input(file_name).int()

    def part1(self):
        spinlock = [0]
        current_position = 0

        for i in range(2017):
            new_position = (current_position + self.step_count) % len(spinlock) + 1
            spinlock.insert(new_position, i+1)
            current_position = new_position

        result = 0

        for i in range(len(spinlock) - 1):
            if spinlock[i] == 2017:
                result = spinlock[i+1]
                break

        print("Part 1:", result)

    def part2(self):
        current_position = 0

        result = 0

        for i in range(50_000_000):
            current_position = (current_position + self.step_count) % (i+1) + 1
            if current_position == 1:
                result = i+1

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D17("2017/17.txt")
    code.part1()
    code.part2()
