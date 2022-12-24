from dataclasses import dataclass
from typing import List

from aoc.util.coordinate import Coordinate, Turtle, TurtleDirection, CoordinateSystem
from aoc.util.graph import Graph, Heuristic
from aoc.util.inputs import Input


def debug(*args, **kwargs):
    if False:
        print(*args, **kwargs)


@dataclass(frozen=True)
class State:
    expedition: Coordinate
    minute: int


class StateHeuristic(Heuristic[Coordinate]):
    def __call__(self, start: State, end: State) -> int:
        return start.expedition.manhattan(end.expedition) * 10 + end.minute - start.minute


class Y2022D24(object):
    """
    The slowest part of this methodology is just moving all the blizzards around and finding the available spots we can
    move between. A lot of that just has to do with the design choice of making all coordinates and turtles immutable
    and therefore a bit expensive as far as python goes.

    The nice bit though is that once the graph is generated, we can go back and forth as many times as we want pretty
    efficiently.

    The idea is pretty simple, we know the blizzards are essentially on a cycle. The overall cycle is the width * height
    of the interior blizzard arena. If we make a directed graph where each node is a location at a certain minute, then
    we can use path planning to find the start to end more easily. Any edge in the digraph is guaranteed to be a valid
    move. We don't have to generate possible states and check if they're valid like we would with a breadth first search.
    """

    def __init__(self, file_name):
        input_grid = Input(file_name).grid()

        # Find all of our blizzards
        blizzards: List[Turtle] = []
        blizzards.extend(Turtle(TurtleDirection.RIGHT, c) for c in input_grid.find('>'))
        blizzards.extend(Turtle(TurtleDirection.LEFT, c) for c in input_grid.find('<'))
        blizzards.extend(Turtle(TurtleDirection.UP, c) for c in input_grid.find('^'))
        blizzards.extend(Turtle(TurtleDirection.DOWN, c) for c in input_grid.find('v'))

        # Let's make a blank grid
        blank_grid = input_grid.copy()
        blizzard: Turtle
        for blizzard in blizzards:
            blank_grid[blizzard.coordinate] = '.'

        movable_spots: set[Coordinate] = set(blank_grid.find('.'))

        cycle = (input_grid.width - 2) * (input_grid.height - 2)

        # We need to be able to use these endpoints in our search while keeping the minute state for all other points.
        # Any time we see the expedition end coordinate, we'll force it to be our end state. Start is a little easier,
        # we just have to start on minute 0.
        expedition_start = Coordinate(1, 0, CoordinateSystem.X_RIGHT_Y_DOWN)
        forced_starting_state = State(
            expedition=expedition_start,
            minute=-1
        )
        expedition_end = Coordinate(input_grid.width - 2, input_grid.height - 1, CoordinateSystem.X_RIGHT_Y_DOWN)
        forced_ending_state = State(
            expedition=expedition_end,
            minute=-1
        )

        graph: Graph[State] = Graph[State](directional=True)
        current_spots = set(input_grid.find('.'))

        for i in range(cycle):
            blizzards = self._next_blizzards(input_grid.width, input_grid.height, blizzards)

            next_spots: set[Coordinate] = set(movable_spots).difference(b.coordinate for b in blizzards)

            debug(f"Generating grid: {i + 1}")
            # next_grid = blank_grid.copy()
            # for b in blizzards:
            #     next_grid[b.coordinate] = 'B'
            # next_grid.to_grid().print()
            # debug()

            next_i = (i + 1) % cycle

            graph.add(State(expedition_start, minute=i), forced_starting_state, weight=0)
            graph.add(State(expedition_end, minute=i), forced_ending_state, weight=0)

            for spot in current_spots:
                starting_state = State(expedition=spot, minute=i)

                if spot in next_spots:  # We can wait here
                    end_state = State(expedition=spot, minute=next_i)
                    graph.add(starting_state, end_state)

                for neighbor in spot.neighbors():
                    if neighbor not in next_spots:
                        continue  # Can't move to our neighbor in the next grid

                    end_state = State(expedition=neighbor, minute=next_i)
                    graph.add(starting_state, end_state)

            current_spots = next_spots

        debug(len(graph.all_nodes))

        zero_starting_state = State(
            expedition=expedition_start,
            minute=0
        )

        path = graph.flood_find(zero_starting_state, forced_ending_state)
        debug(path)
        # -2 because we're counting minute 0 when we don't need it, as well as our forced end
        self.first_pass_through = len(path) - 2
        debug(self.first_pass_through)
        debug()

        new_end = path[-2]  # Skip our forced end to get the real end
        path = graph.flood_find(new_end, forced_starting_state)
        debug(path)
        # -2 because we're counting our new_end when we don't need it, as well as our forced start
        back_to_start = len(path) - 2
        debug(back_to_start)

        new_start = path[-2]  # Skip our forced start to get the real start
        path = graph.flood_find(new_start, forced_ending_state)
        debug(path)
        # -2 because we're counting our new_start when we don't need it, as well as our forced end
        back_to_end = len(path) - 2
        debug(back_to_end)

        self.total_journey = self.first_pass_through + back_to_start + back_to_end

    @staticmethod
    def _next_blizzards(width: int, height: int, blizzards: List[Turtle]) -> List[Turtle]:
        result = []

        for blizzard in blizzards:
            next_blizzard = blizzard.forward()
            if next_blizzard.coordinate.x == width - 1:
                next_blizzard = Turtle(
                    direction=TurtleDirection.RIGHT,
                    coordinate=Coordinate(1, next_blizzard.coordinate.y, CoordinateSystem.X_RIGHT_Y_DOWN)
                )
            elif next_blizzard.coordinate.x == 0:
                next_blizzard = Turtle(
                    direction=TurtleDirection.LEFT,
                    coordinate=Coordinate(width - 2, next_blizzard.coordinate.y, CoordinateSystem.X_RIGHT_Y_DOWN)
                )
            elif next_blizzard.coordinate.y == height - 1:
                next_blizzard = Turtle(
                    direction=TurtleDirection.DOWN,
                    coordinate=Coordinate(next_blizzard.coordinate.x, 1, CoordinateSystem.X_RIGHT_Y_DOWN)
                )
            elif next_blizzard.coordinate.y == 0:
                next_blizzard = Turtle(
                    direction=TurtleDirection.UP,
                    coordinate=Coordinate(next_blizzard.coordinate.x, height - 2, CoordinateSystem.X_RIGHT_Y_DOWN)
                )

            result.append(next_blizzard)

        return result

    def part1(self):
        result = self.first_pass_through

        print("Part 1:", result)

    def part2(self):
        # Can't believe an elf left their snacks. I bet it's that massive elf nerd Geoffrey
        result = self.total_journey

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D24("2022/24.txt")
    code.part1()
    code.part2()
