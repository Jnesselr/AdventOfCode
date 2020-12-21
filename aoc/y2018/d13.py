from enum import Enum
from typing import Set, List, Tuple, Dict

from aoc.util.coordinate import TurtleDirection, Turtle, Coordinate
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Turn(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

class CartMadness(object):
    def __init__(self, grid: Grid[str]):
        self.grid: Grid[str] = grid
        self.carts: Set[Turtle] = set()
        self.crashes: List[Coordinate] = []
        self._next_turn: Dict[Turtle, Turn] = {}

        for coordinate, value in self.grid.items():
            if value not in 'v><^':
                continue

            if value == 'v':
                direction = TurtleDirection.DOWN
                self.grid[coordinate] = '|'
            elif value == '^':
                direction = TurtleDirection.UP
                self.grid[coordinate] = '|'
            elif value == '<':
                direction = TurtleDirection.LEFT
                self.grid[coordinate] = '-'
            elif value == '>':
                direction = TurtleDirection.RIGHT
                self.grid[coordinate] = '-'
            else:
                raise ValueError("We should never get here, oh noes!")

            cart = Turtle(direction, coordinate)
            self.carts.add(cart)
            self._next_turn[cart] = Turn.LEFT

    def run(self):
        while len(self.carts) > 1:
            # DEBUG

            # new_grid = self.grid.copy()
            # for cart in self.carts:
            #     if cart.direction == TurtleDirection.UP:
            #         new_grid[cart.coordinate] = '^'
            #     elif cart.direction == TurtleDirection.DOWN:
            #         new_grid[cart.coordinate] = 'v'
            #     elif cart.direction == TurtleDirection.LEFT:
            #         new_grid[cart.coordinate] = '<'
            #     elif cart.direction == TurtleDirection.RIGHT:
            #         new_grid[cart.coordinate] = '>'
            # new_grid.print()
            # print()

            #DEBUG

            ordered_carts = sorted(list(self.carts), key=lambda x: x.coordinate)
            for cart in ordered_carts:
                if cart not in self.carts:
                    continue  # Destroyed before your turn

                self.carts.remove(cart)
                turn = self._next_turn[cart]

                new_cart = cart.forward()
                crashed = False
                for other_cart in self.carts.copy():
                    if other_cart.coordinate == new_cart.coordinate:
                        crashed = True
                        self.carts.remove(other_cart)
                        del self._next_turn[other_cart]
                        self.crashes.append(new_cart.coordinate)

                if crashed:
                    continue

                if self.grid[new_cart.coordinate] == '\\':
                    if new_cart.direction == TurtleDirection.RIGHT:
                        new_cart = new_cart.turn_right()
                    elif new_cart.direction == TurtleDirection.LEFT:
                        new_cart = new_cart.turn_right()
                    elif new_cart.direction == TurtleDirection.UP:
                        new_cart = new_cart.turn_left()
                    elif new_cart.direction == TurtleDirection.DOWN:
                        new_cart = new_cart.turn_left()
                elif self.grid[new_cart.coordinate] == '/':
                    if new_cart.direction == TurtleDirection.RIGHT:
                        new_cart = new_cart.turn_left()
                    elif new_cart.direction == TurtleDirection.LEFT:
                        new_cart = new_cart.turn_left()
                    elif new_cart.direction == TurtleDirection.UP:
                        new_cart = new_cart.turn_right()
                    elif new_cart.direction == TurtleDirection.DOWN:
                        new_cart = new_cart.turn_right()
                elif self.grid[new_cart.coordinate] == '+':
                    if turn == Turn.LEFT:
                        new_cart = new_cart.turn_left()
                        turn = turn.STRAIGHT
                    elif turn == Turn.STRAIGHT:
                        turn = turn.RIGHT
                    elif turn == Turn.RIGHT:
                        new_cart = new_cart.turn_right()
                        turn = turn.LEFT

                self.carts.add(new_cart)
                self._next_turn[new_cart] = turn


class Y2018D13(object):
    def __init__(self, file_name):
        self.madness = CartMadness(Input(file_name).grid())
        self.madness.run()

    def part1(self):
        crash = self.madness.crashes[0]
        result = f"{crash.x},{crash.y}"

        print("Part 1:", result)

    def part2(self):
        last_cart = list(self.madness.carts)[0]
        result = f"{last_cart.coordinate.x},{last_cart.coordinate.y}"

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2018D13("2018/13.txt")
    code.part1()
    code.part2()
