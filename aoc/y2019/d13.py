from enum import Enum

from aoc.util.grid import InfiniteGrid
from aoc.util.intcode import Intcode


class Tile(Enum):
    EMPTY = (0, ' ')
    WALL = (1, '#')
    BLOCK = (2, '*')
    PADDLE = (3, '-')
    BALL = (4, '@')

    def __init__(self, tile_id, character):
        self.tile_id = tile_id
        self.character = character

    @classmethod
    def from_id(cls, _id):
        for member in cls._member_map_.values():
            if member.tile_id == _id:
                return member


class Y2019D13(object):
    def __init__(self, file_name):
        self.arcade = Intcode(file_name)
        self.grid: InfiniteGrid[Tile] = InfiniteGrid[Tile]()
        self.score = 0

    def reset(self):
        self.score = 0
        self.grid.clear()
        self.arcade.reset()

    def _get_game_update(self):
        while self.arcade.has_output:
            x = self.arcade.output()
            y = self.arcade.output()
            tile_id = self.arcade.output()

            if x == -1 and y == 0:
                self.score = tile_id
            else:
                self.grid[x, y] = Tile.from_id(tile_id)

        # self.grid.to_grid().print(key=lambda x: x.character)

    def part1(self):
        self.reset()
        self.arcade.run()
        self._get_game_update()
        result = len(self.grid.find(Tile.BLOCK))

        print("Part 1:", result)

    def part2(self):
        self.reset()
        self.arcade.ram[0] = 2
        self.arcade.run()
        self._get_game_update()

        while not self.arcade.halted:
            ball = self.grid.find(Tile.BALL)[0]
            paddle = self.grid.find(Tile.PADDLE)[0]
            # Move the paddle if needed

            if ball.x > paddle.x:
                self.arcade.input(1)
            elif ball.x < paddle.x:
                self.arcade.input(-1)
            else:
                self.arcade.input(0)

            self._get_game_update()

        print("Part 2:", self.score)


if __name__ == '__main__':
    code = Y2019D13("2019/13.txt")
    code.part1()
    code.part2()
