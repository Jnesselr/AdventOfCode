from queue import Queue
from typing import Optional

from aoc.util.coordinate import Coordinate, Turtle, TurtleDirection
from aoc.util.graph import Graph, TurtleHeuristic
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2024D16(object):
    def __init__(self, file_name):
        self._grid = Input(file_name).grid()
        starting_coordinate: Coordinate = self._grid.find('S')[0]
        ending_coordinate: Coordinate = self._grid.find('E')[0]
        self._grid[starting_coordinate] = '.'
        self._grid[ending_coordinate] = '.'

        self._starting_turtle: Turtle = Turtle(TurtleDirection.EAST, starting_coordinate)
        self._ending_turtle: Turtle = Turtle(TurtleDirection.EAST, ending_coordinate)
        self._graph = self._graph_from_grid()

    def _find_path_from_node(self, starting_node: Turtle) -> Optional[list[Turtle]]:
        heuristic = TurtleHeuristic()
        return self._graph.find_path(starting_node, self._ending_turtle, heuristic)

    def part1(self):
        path = self._find_path_from_node(self._starting_turtle)
        result = self._graph.get_weight(path)

        print("Part 1:", result)

    def part2(self):
        all_nodes = self._graph.get_all_nodes_with_shortest_path(self._starting_turtle, self._find_path_from_node)
        all_coordinates = set(t.coordinate for t in all_nodes)
        result = len(all_coordinates)

        print("Part 2:", result)

    def _graph_from_grid(self) -> Graph[Turtle]:
        graph: Graph[Turtle] = Graph(directional=True)

        def _add_turn(coordinate: Coordinate, a: TurtleDirection, b: TurtleDirection, turn_weight=1000):
            graph.add(Turtle(a, coordinate), Turtle(b, coordinate), turn_weight)

        for current in self._grid.find('.'):
            up_valid = self._grid[up := current.up()] == '.'
            down_valid = self._grid[down := current.down()] == '.'
            left_valid = self._grid[left := current.left()] == '.'
            right_valid = self._grid[right := current.right()] == '.'
            # Straight moves
            if up_valid:
                graph.add(
                    Turtle(TurtleDirection.UP, current),
                    Turtle(TurtleDirection.UP, up)
                )
            if down_valid:
                graph.add(
                    Turtle(TurtleDirection.DOWN, current),
                    Turtle(TurtleDirection.DOWN, down)
                )
            if left_valid:
                graph.add(
                    Turtle(TurtleDirection.LEFT, current),
                    Turtle(TurtleDirection.LEFT, left)
                )
            if right_valid:
                graph.add(
                    Turtle(TurtleDirection.RIGHT, current),
                    Turtle(TurtleDirection.RIGHT, right)
                )

            # Turning moves
            if up_valid and right_valid:
                _add_turn(current, TurtleDirection.LEFT, TurtleDirection.UP)
                _add_turn(current, TurtleDirection.DOWN, TurtleDirection.RIGHT)
            if right_valid and down_valid:
                _add_turn(current, TurtleDirection.LEFT, TurtleDirection.DOWN)
                _add_turn(current, TurtleDirection.UP, TurtleDirection.RIGHT)
            if down_valid and left_valid:
                _add_turn(current, TurtleDirection.UP, TurtleDirection.LEFT)
                _add_turn(current, TurtleDirection.RIGHT, TurtleDirection.DOWN)
            if left_valid and up_valid:
                _add_turn(current, TurtleDirection.RIGHT, TurtleDirection.UP)
                _add_turn(current, TurtleDirection.DOWN, TurtleDirection.LEFT)

        _add_turn(self._starting_turtle.coordinate, TurtleDirection.EAST, TurtleDirection.UP)
        _add_turn(self._starting_turtle.coordinate, TurtleDirection.EAST, TurtleDirection.DOWN)
        _add_turn(self._starting_turtle.coordinate, TurtleDirection.UP, TurtleDirection.LEFT)

        # All roads lead to the same ending turtle
        _add_turn(self._ending_turtle.coordinate, TurtleDirection.UP, TurtleDirection.RIGHT, 0)
        _add_turn(self._ending_turtle.coordinate, TurtleDirection.LEFT, TurtleDirection.RIGHT, 0)
        _add_turn(self._ending_turtle.coordinate, TurtleDirection.DOWN, TurtleDirection.RIGHT, 0)

        return graph


if __name__ == '__main__':
    code = Y2024D16("2024/16.txt")
    code.part1()
    code.part2()
