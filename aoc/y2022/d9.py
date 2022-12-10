from aoc.util.coordinate import Coordinate
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2022D9(object):
    def __init__(self, file_name):
        self.lines = Input(file_name).lines()

    def part1(self):
        result = self.get_tail_coverage(2)

        print("Part 1:", result)

    def part2(self):
        result = self.get_tail_coverage(10)

        print("Part 2:", result)

    def get_tail_coverage(self, rope_length: int) -> int:
        move_grid = InfiniteGrid[str]()

        rope = [Coordinate(0, 0)] * rope_length
        tail_position = Coordinate(0, 0)

        move_grid[tail_position] = '#'

        for line in self.lines:
            move, count = line.split(' ')
            for _ in range(int(count)):
                if move == 'U':
                    rope[0] = rope[0].up()
                elif move == 'D':
                    rope[0] = rope[0].down()
                elif move == 'R':
                    rope[0] = rope[0].right()
                elif move == 'L':
                    rope[0] = rope[0].left()

                for index in range(0, rope_length - 1):
                    head_position = rope[index]
                    tail_position = rope[index + 1]

                    tail_left = tail_position.left()
                    tail_right = tail_position.right()
                    tail_up = tail_position.up()
                    tail_down = tail_position.down()
                    good_head_positions = {
                        tail_left.up(),
                        tail_up,
                        tail_right.up(),
                        tail_left,
                        tail_position,
                        tail_right,
                        tail_left.down(),
                        tail_down,
                        tail_right.down()
                    }

                    if head_position not in good_head_positions:
                        if head_position.x < tail_position.x:
                            tail_position = tail_left
                        elif head_position.x > tail_position.x:
                            tail_position = tail_right

                        if head_position.y < tail_position.y:
                            tail_position = tail_position.down()
                        elif head_position.y > tail_position.y:
                            tail_position = tail_position.up()

                    rope[index] = head_position
                    rope[index + 1] = tail_position

                move_grid[rope[rope_length - 1]] = '#'

            # print(line)
            # print(head_position)
            # print(tail_position)
            # self.move_grid.to_grid().print(not_found='.')
            # print()

        return len(move_grid.find('#'))


if __name__ == '__main__':
    code = Y2022D9("2022/9.txt")
    code.part1()
    code.part2()
