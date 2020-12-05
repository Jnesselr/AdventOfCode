from aoc.util.inputs import Input


class Y2020D5(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.seats_ids = []

        for line in lines:
            row, col = self._get_seat(line)
            self.seats_ids.append(row * 8 + col)

        self.seats_ids = sorted(self.seats_ids)

    @staticmethod
    def _get_seat(seat_instruction):
        row_min = 0
        row_max = 127
        for i in seat_instruction[:7]:
            if i == 'F':
                row_max = (row_min + row_max) // 2
            elif i == 'B':
                row_min = (row_min + row_max + 1) // 2
        col_min = 0
        col_max = 7
        for i in seat_instruction[7:]:
            if i == 'L':
                col_max = (col_min + col_max) // 2
            elif i == 'R':
                col_min = (col_min + col_max + 1) // 2

        return row_min, col_min

    def part1(self):
        result = self.seats_ids[-1]

        print("Part 1:", result)

    def part2(self):
        min_id = self.seats_ids[0]
        max_id = self.seats_ids[-1]

        result = 0

        for i in range(min_id, max_id):
            if i not in self.seats_ids:
                result = i

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D5("2020/5.txt")
    code.part1()
    code.part2()
