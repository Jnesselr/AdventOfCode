from queue import Queue

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2024D15(object):
    _debug = False

    def __init__(self, file_name):
        groups = Input(file_name).grouped()
        self._grid_start: Grid[str] = Grid.from_str(groups[0])
        self._moves: str = ''.join(groups[1])
        self._robot_start: Coordinate = self._grid_start.find('@')[0]
        self._grid_start[self._robot_start] = '.'

    def part1(self):
        grid = self._grid_start.copy()
        robot = self._robot_start
        for move in self._moves:
            check = robot.move(move)
            mapping = {check: robot}  # robot moves to check
            while grid[check] not in '.#':
                new_check = check.move(move)
                mapping[new_check] = check
                check = new_check

            if grid[check] == '#':
                continue  # Hit a wall, nothing more to do

            if self._debug:
                print(move, mapping)
            while len(mapping) >= 2:
                to_space, from_space = mapping.popitem()
                grid[to_space] = grid[from_space]
                grid[from_space] = '.'

            robot, _ = mapping.popitem()
            if self._debug:
                grid[robot] = '@'
                grid.print()
                grid[robot] = '.'
                print()

        boxes = grid.find('O')
        result = sum(b.y * 100 + b.x for b in boxes)

        print("Part 1:", result)

    def part2(self):
        wide_grid = Grid[str](2 * self._grid_start.width, self._grid_start.height)
        for coordinate, value in self._grid_start.items():
            new_value = {
                '#': '##',
                'O': '[]',
                '.': '..',
            }[value]
            wide_grid[2 * coordinate.x, coordinate.y] = new_value[0]
            wide_grid[2 * coordinate.x + 1, coordinate.y] = new_value[1]

        robot = Coordinate(
            x=self._robot_start.x * 2,
            y=self._robot_start.y,
            system=CoordinateSystem.X_RIGHT_Y_DOWN
        )

        if self._debug:
            wide_grid[robot] = '@'
            wide_grid.print()
            wide_grid[robot] = '.'
            print()

        magic_free_space = Coordinate(-1, -1, system=CoordinateSystem.X_RIGHT_Y_DOWN)

        for move in self._moves:
            mapping = {}
            q = Queue()
            q.put(robot)
            is_blocked = False
            while not q.empty():
                to_check: Coordinate = q.get()
                next_move = to_check.move(move)
                mapping[next_move] = to_check
                grid_value: str = wide_grid[next_move]
                if grid_value == '#':
                    is_blocked = True
                    break

                if grid_value == '.':
                    continue  # Open space, not pushing on anything else

                q.put(next_move)  # Need to check next_move regardless
                if move in '<>':
                    # These are easy, we can just ignore that we might be moving a box as a whole
                    continue

                # next_move is up or down at this point
                if grid_value == '[':  # Left side of box
                    right = next_move.right()
                    q.put(right)
                elif grid_value == ']':  # Right side of box
                    left = next_move.left()
                    q.put(left)
                else:
                    raise Exception("Unexpected block value")

            if is_blocked:
                continue  # Hit a wall, nothing more to do

            if self._debug:
                print(move, mapping)
            while len(mapping) >= 2:
                to_space, from_space = mapping.popitem()
                if from_space != magic_free_space:
                    wide_grid[to_space] = wide_grid[from_space]
                    wide_grid[from_space] = '.'
                else:
                    wide_grid[to_space] = '.'

            robot, _ = mapping.popitem()
            if self._debug:
                wide_grid[robot] = '@'
                wide_grid.print()
                wide_grid[robot] = '.'
                print()

        boxes = wide_grid.find('[')
        result = sum(b.y * 100 + b.x for b in boxes)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2024D15("2024/15.txt")
    code.part1()
    code.part2()
