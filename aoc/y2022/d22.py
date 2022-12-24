import abc
import enum
import re
from collections import defaultdict
from itertools import product
from queue import Queue
from typing import Dict, Union, List, Iterator, Optional

from math import gcd

from aoc.util.coordinate import Coordinate, CoordinateSystem, Turtle, TurtleDirection
from aoc.util.graph import Graph
from aoc.util.grid import Grid
from aoc.util.inputs import Input

Instruction = Union[int, str]


def debug(*args, **kwargs):
    if False:
        print(*args, **kwargs)


class MoveOption(enum.Enum):
    """
    We use the move option as the weight in the graph. Then we can select the edges and only move
    if there's a weight that matches the action we're trying to take.
    """
    MOVE_FORWARD = 0
    TURN_RIGHT = 1
    TURN_LEFT = 2


class Teleporter(abc.ABC):
    def __init__(self, grid: Grid[str]):
        # By default, we want to copy the grid in case a subclass modifies it
        self.grid = grid.copy()
        self.graph: Graph[Turtle] = Graph[Turtle](directional=True)
        starting_coordinate = Coordinate(1_000, 1_000, CoordinateSystem.X_RIGHT_Y_DOWN)

        # Go through each coordinate and build out our basic graph without teleporting
        for coordinate, value in self.grid.items():
            if value == '#':  # If we're a wall, no need to bother
                continue

            if coordinate.y < starting_coordinate.y:
                starting_coordinate = coordinate
            if coordinate.y == starting_coordinate.y and coordinate.x < starting_coordinate.x:
                starting_coordinate = coordinate

            # Turtles facing the direction we care about all on the same coordinate
            turtle_right = Turtle(TurtleDirection.RIGHT, coordinate)
            turtle_down = Turtle(TurtleDirection.DOWN, coordinate)
            turtle_left = Turtle(TurtleDirection.LEFT, coordinate)
            turtle_up = Turtle(TurtleDirection.UP, coordinate)

            # Start by making sure we can spin in place clockwise
            self.graph.add(turtle_right, turtle_down, MoveOption.TURN_RIGHT)
            self.graph.add(turtle_down, turtle_left, MoveOption.TURN_RIGHT)
            self.graph.add(turtle_left, turtle_up, MoveOption.TURN_RIGHT)
            self.graph.add(turtle_up, turtle_right, MoveOption.TURN_RIGHT)

            # And counter-clockwise
            self.graph.add(turtle_right, turtle_up, MoveOption.TURN_LEFT)
            self.graph.add(turtle_up, turtle_left, MoveOption.TURN_LEFT)
            self.graph.add(turtle_left, turtle_down, MoveOption.TURN_LEFT)
            self.graph.add(turtle_down, turtle_right, MoveOption.TURN_LEFT)

            # These turtles have advanced one step in their respective directions
            turtle_moved_right = turtle_right.forward()
            turtle_moved_down = turtle_down.forward()
            turtle_moved_left = turtle_left.forward()
            turtle_moved_up = turtle_up.forward()

            if grid[turtle_moved_right.coordinate] == '.':
                self.graph.add(turtle_right, turtle_moved_right, MoveOption.MOVE_FORWARD)

            if grid[turtle_moved_down.coordinate] == '.':
                self.graph.add(turtle_down, turtle_moved_down, MoveOption.MOVE_FORWARD)

            if grid[turtle_moved_left.coordinate] == '.':
                self.graph.add(turtle_left, turtle_moved_left, MoveOption.MOVE_FORWARD)

            if grid[turtle_moved_up.coordinate] == '.':
                self.graph.add(turtle_up, turtle_moved_up, MoveOption.MOVE_FORWARD)

        self._starting_turtle = Turtle(
            direction=TurtleDirection.RIGHT,
            coordinate=starting_coordinate
        )

    @staticmethod
    def _instruction_iterator(instructions: List[Instruction]) -> Iterator[MoveOption]:
        for instruction in instructions:
            if instruction == 'R':
                yield MoveOption.TURN_RIGHT
            elif instruction == 'L':
                yield MoveOption.TURN_LEFT
            else:  # Move forward `instruction` times
                for _ in range(instruction):
                    yield MoveOption.MOVE_FORWARD

    def run_instructions(self, instructions: List[Instruction]) -> int:
        turtle = self._starting_turtle

        move_option: MoveOption
        for move_option in self._instruction_iterator(instructions):
            self.grid[turtle.coordinate] = turtle.direction.symbol

            edges_from_current = self.graph.edges_from(turtle)
            edges_we_care_about = [edge for edge in edges_from_current if edge.weight == move_option]
            maybe_edge = edges_we_care_about[0] if edges_we_care_about else None

            if maybe_edge is None:
                continue  # Cannot perform this step

            turtle = maybe_edge.end

        direction_score = {
            TurtleDirection.RIGHT: 0,
            TurtleDirection.DOWN: 1,
            TurtleDirection.LEFT: 2,
            TurtleDirection.UP: 3,
        }[turtle.direction]

        result = (turtle.coordinate.y + 1) * 1000
        result += (turtle.coordinate.x + 1) * 4
        result += direction_score

        return result


class SimpleTeleporter(Teleporter):
    def __init__(self, grid: Grid[str]):
        super().__init__(grid)

        by_column_min: Dict[int, int] = defaultdict(lambda: 1_000)
        by_column_max: Dict[int, int] = defaultdict(lambda: -1_000)
        by_row_min: Dict[int, int] = defaultdict(lambda: 1_000)
        by_row_max: Dict[int, int] = defaultdict(lambda: -1_000)

        for coordinate in grid:
            by_column_min[coordinate.x] = min(by_column_min[coordinate.x], coordinate.y)
            by_column_max[coordinate.x] = max(by_column_max[coordinate.x], coordinate.y)
            by_row_min[coordinate.y] = min(by_row_min[coordinate.y], coordinate.x)
            by_row_max[coordinate.y] = max(by_row_max[coordinate.y], coordinate.x)

        for column in range(grid.min_x, grid.max_x + 1):
            top = by_column_min[column]
            bottom = by_column_max[column]

            if grid[column, top] == '#' or grid[column, bottom] == '#':
                continue  # Can't link to a wall

            top_coordinate = Coordinate(column, top, CoordinateSystem.X_RIGHT_Y_DOWN)
            bottom_coordinate = Coordinate(column, bottom, CoordinateSystem.X_RIGHT_Y_DOWN)

            top_turtle_facing_up = Turtle(TurtleDirection.UP, top_coordinate)
            top_turtle_facing_down = Turtle(TurtleDirection.DOWN, top_coordinate)
            bottom_turtle_facing_up = Turtle(TurtleDirection.UP, bottom_coordinate)
            bottom_turtle_facing_down = Turtle(TurtleDirection.DOWN, bottom_coordinate)

            self.graph.add(top_turtle_facing_up, bottom_turtle_facing_up, MoveOption.MOVE_FORWARD)
            self.graph.add(bottom_turtle_facing_down, top_turtle_facing_down, MoveOption.MOVE_FORWARD)

        for row in range(grid.min_y, grid.max_y + 1):
            left = by_row_min[row]
            right = by_row_max[row]

            if grid[left, row] == '#' or grid[right, row] == '#':
                continue  # Can't link to a wall

            left_coordinate = Coordinate(left, row, CoordinateSystem.X_RIGHT_Y_DOWN)
            right_coordinate = Coordinate(right, row, CoordinateSystem.X_RIGHT_Y_DOWN)

            left_turtle_facing_left = Turtle(TurtleDirection.LEFT, left_coordinate)
            left_turtle_facing_right = Turtle(TurtleDirection.RIGHT, left_coordinate)
            right_turtle_facing_left = Turtle(TurtleDirection.LEFT, right_coordinate)
            right_turtle_facing_right = Turtle(TurtleDirection.RIGHT, right_coordinate)

            self.graph.add(left_turtle_facing_left, right_turtle_facing_left, MoveOption.MOVE_FORWARD)
            self.graph.add(right_turtle_facing_right, left_turtle_facing_right, MoveOption.MOVE_FORWARD)


class CubeTeleporter(Teleporter):
    """
    This algorithm is annoying and complicated, but it's designed to fold any sized cube. Essentially, we find a corner
    and start zipping up the sides. Since you can never have 2 segments at a right angle that are twice the length of
    the actual size of the cube, we essentially go until we can't go anymore, then evaluate what state each side of the
    zipper is on, and then continue until we're all zipped up.

    To expound on "go until we can't go anymore", you cannot have two faces joined by more than one side. So if that's
    about to happen, we abort the zipping process and find another corner. You can also have it where the same coordinate
    might be zipped twice accidentally. This should technically be fine as far as the run instructions step goes, it
    just means there will be two edges between the same two nodes with the same move option. Not a huge deal and easier
    than figuring out if a coordinate is seen already or not when we have to rotate on the spot.
    """

    def __init__(self, grid: Grid[str]):
        super().__init__(grid)

        self._coordinates_to_face: Dict[Coordinate, int] = self._get_coordinates_to_face()

        self._zip_it_all_up()

    def _get_coordinates_to_face(self) -> Dict[Coordinate, int]:
        result: Dict[Coordinate, int] = {}

        # The cube laid out should have one dimension that is 1, 2, or 3. You cannot lay it out in a 4x4 or a 2x4.
        # This means the greatest common divisor is the face size
        face_size = gcd(self.grid.width, self.grid.height)

        seen = set()
        q = Queue()
        q.put(self._starting_turtle.coordinate)
        seen.add(self._starting_turtle.coordinate)
        index = 0

        while not q.empty():
            top_left: Coordinate = q.get()
            index += 1

            for diff_x, diff_y in product(range(face_size), repeat=2):
                new_coord = top_left.right(diff_x).down(diff_y)
                result[new_coord] = index

            left_face_top_left = top_left.left(face_size)
            if left_face_top_left in self.grid and left_face_top_left not in seen:
                seen.add(left_face_top_left)
                q.put(left_face_top_left)

            right_face_top_left = top_left.right(face_size)
            if right_face_top_left in self.grid and right_face_top_left not in seen:
                seen.add(right_face_top_left)
                q.put(right_face_top_left)

            down_face_top_left = top_left.down(face_size)
            if down_face_top_left in self.grid and down_face_top_left not in seen:
                seen.add(down_face_top_left)
                q.put(down_face_top_left)

            # We don't need to go up at all, we're always working our way down the grid

        return result

    def _zip_it_all_up(self):
        for inside_corner in self._get_inside_corners():
            debug("Inside corner:", inside_corner)

            zipper_a: Optional[Turtle] = None
            zipper_b: Optional[Turtle] = None
            a_exterior: Optional[TurtleDirection] = None
            b_interior: Optional[TurtleDirection] = None

            left = inside_corner.left()
            right = inside_corner.right()
            up = inside_corner.up()
            down = inside_corner.down()
            left_up = left.up()
            left_down = left.down()
            right_up = right.up()
            right_down = right.down()

            if left_up not in self.grid:
                zipper_a = Turtle(TurtleDirection.UP, up)
                a_exterior = TurtleDirection.LEFT
                zipper_b = Turtle(TurtleDirection.LEFT, left)
                b_interior = TurtleDirection.DOWN
            elif left_down not in self.grid:
                zipper_a = Turtle(TurtleDirection.LEFT, left)
                a_exterior = TurtleDirection.DOWN
                zipper_b = Turtle(TurtleDirection.DOWN, down)
                b_interior = TurtleDirection.RIGHT
            elif right_up not in self.grid:
                zipper_a = Turtle(TurtleDirection.RIGHT, right)
                a_exterior = TurtleDirection.UP
                zipper_b = Turtle(TurtleDirection.UP, up)
                b_interior = TurtleDirection.LEFT
            elif right_down not in self.grid:
                zipper_a = Turtle(TurtleDirection.DOWN, down)
                a_exterior = TurtleDirection.RIGHT
                zipper_b = Turtle(TurtleDirection.RIGHT, right)
                b_interior = TurtleDirection.UP

            self._zip_up_from_corner(zipper_a, a_exterior, zipper_b, b_interior)

    def _zip_up_from_corner(self, zipper_a, a_exterior, zipper_b, b_interior):
        current_face_a = self._coordinates_to_face[zipper_a.coordinate]
        current_face_b = self._coordinates_to_face[zipper_b.coordinate]

        while True:
            a_turtle = Turtle(a_exterior, zipper_a.coordinate)
            b_turtle = Turtle(b_interior, zipper_b.coordinate)
            if self.grid[a_turtle.coordinate] == '.' and self.grid[b_turtle.coordinate] == '.':
                debug(f"Binding {a_turtle} to {b_turtle}")
                a_turtle_opposite = Turtle(a_exterior.opposite(), zipper_a.coordinate)
                b_turtle_opposite = Turtle(b_interior.opposite(), zipper_b.coordinate)

                self.graph.add(a_turtle, b_turtle, MoveOption.MOVE_FORWARD)
                self.graph.add(b_turtle_opposite, a_turtle_opposite, MoveOption.MOVE_FORWARD)
            next_zipper_a = zipper_a.forward()
            next_zipper_b = zipper_b.forward()

            evaluate_current_state = False
            evaluate_current_state |= next_zipper_a.coordinate not in self.grid
            evaluate_current_state |= next_zipper_b.coordinate not in self.grid
            evaluate_current_state |= next_zipper_a.my_left() in self.grid and next_zipper_a.my_right() in self.grid
            evaluate_current_state |= next_zipper_b.my_left() in self.grid and next_zipper_b.my_right() in self.grid

            if evaluate_current_state:
                debug("Oh we should re-evaluate!")
                next_zipper_a, a_exterior = self._re_evaluate(
                    zipper_a,
                    a_exterior)
                next_zipper_b, b_interior = self._re_evaluate(
                    zipper_b,
                    b_interior
                )
                debug("Next A:", next_zipper_a)
                debug("A Exterior:", a_exterior)
                debug("Next B:", next_zipper_b)
                debug("B Interior:", b_interior)
                debug()

                next_face_a = self._coordinates_to_face[next_zipper_a.coordinate]
                next_face_b = self._coordinates_to_face[next_zipper_b.coordinate]

                if next_face_a == current_face_a and next_face_b == current_face_b:
                    # Can't zip two edges on the same two faces together.
                    debug("Just kidding, we can't zip those up")
                    return

                current_face_a = next_face_a
                current_face_b = next_face_b

            zipper_a = next_zipper_a
            zipper_b = next_zipper_b

    def _get_inside_corners(self) -> Iterator[Coordinate]:
        coordinate: Coordinate
        for coordinate in self.grid:
            left = coordinate.left()
            right = coordinate.right()
            left_up = left.up()
            left_down = left.down()
            right_up = right.up()
            right_down = right.down()

            adjacent_in_count = sum([
                1 if left_up in self.grid else 0,
                1 if left_down in self.grid else 0,
                1 if right_up in self.grid else 0,
                1 if right_down in self.grid else 0,
            ])

            if adjacent_in_count != 3:
                continue  # We need 3 corners to be there, 1 missing

            # We're potentially a corner or one out from each leg of the corner so narrow it down more
            up = coordinate.up()
            down = coordinate.down()

            adjacent_in_count = sum([
                1 if left in self.grid else 0,
                1 if right in self.grid else 0,
                1 if up in self.grid else 0,
                1 if down in self.grid else 0,
            ])

            if adjacent_in_count != 4:
                continue  # An interior corner has all it's direct adjacent neighbors

            yield coordinate

    def _re_evaluate(self,
                     zipper: Turtle,
                     facing_direction: TurtleDirection):
        forward_zipper = zipper.forward()

        if forward_zipper.coordinate not in self.grid:
            """
            In this case, we've hit an edge head on. This has to be an exterior corner. We simply turn in place
            depending on if my_right or my_left are in the grid.
            """
            if zipper.my_left() in self.grid:
                return zipper.turn_left(), facing_direction.turn_left()
            else:
                return zipper.turn_right(), facing_direction.turn_right()

        # From this point on, forward_zipper must be in the grid
        forward_right = forward_zipper.my_right()
        forward_left = forward_zipper.my_left()
        if forward_right in self.grid and forward_left in self.grid:
            """
            Essentially, we've hit another interior corner. If zipper's right is not there, then forward zipper turns
            right and moves forward one. If zipper's left is not there, forward zipper turns left and moves forward. The
            facing direction makes the same turn.
            """
            if zipper.my_left() not in self.grid:
                return forward_zipper.turn_left().forward(), facing_direction.turn_left()
            else:
                return forward_zipper.turn_right().forward(), facing_direction.turn_right()

        # At this point, the only real case is continuing straight on.
        return forward_zipper, facing_direction


class Y2022D22(object):
    def __init__(self, file_name):
        grid_string, instruction_string = Input(file_name).grouped()
        self.instructions = []
        instruction_string = instruction_string[0]

        instruction_regex = re.compile(r'(\d+|[RL])')
        while match := instruction_regex.match(instruction_string):
            next_instruction = match.group(1)
            if next_instruction not in 'RL':
                next_instruction = int(next_instruction)

            self.instructions.append(next_instruction)
            instruction_string = instruction_string[match.end():]

        self.grid = Grid.from_str(grid_string)

        for coordinate in self.grid.find(' '):
            del self.grid[coordinate]

    def part1(self):
        teleporter = SimpleTeleporter(self.grid)
        result = teleporter.run_instructions(self.instructions)

        print("Part 1:", result)

    def part2(self):
        teleporter = CubeTeleporter(self.grid)
        result = teleporter.run_instructions(self.instructions)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D22("2022/22.txt")
    code.part1()
    code.part2()
