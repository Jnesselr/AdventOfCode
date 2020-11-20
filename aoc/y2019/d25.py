import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Set, List, Optional, Tuple

from aoc.util.intcode import Intcode


class CurrentlyReading(Enum):
    Nothing = auto()
    Description = auto()
    Doors = auto()
    Items = auto()


@dataclass(frozen=True)
class DungeonLocation(object):
    name: str
    description: str
    doors_here_lead: Set[str]
    items: Set[str]

    @staticmethod
    def read(output: str):
        output = output.split('\n')
        name = None
        description = ""
        doors_here_lead: Set[str] = set()
        items: Set[str] = set()

        reading = CurrentlyReading.Nothing
        for line in output:
            if line == "":
                reading = CurrentlyReading.Nothing
            elif reading == CurrentlyReading.Nothing:
                if line.startswith("=="):
                    name = line[3:-3]
                    reading = CurrentlyReading.Description  # Description always comes after name
                elif line == "Doors here lead:":
                    reading = CurrentlyReading.Doors
                elif line == "Items here:":
                    reading = CurrentlyReading.Items
            elif reading == CurrentlyReading.Description:
                description = line
            elif reading == CurrentlyReading.Doors:
                doors_here_lead.add(line[2:])
            elif reading == CurrentlyReading.Items:
                items.add(line[2:])

        return DungeonLocation(
            name=name,
            description=description,
            doors_here_lead=doors_here_lead,
            items=items
        )


class Y2019D25(object):
    def __init__(self, file_name):
        self.computer = Intcode(file_name)
        self._do_not_take = [
            "escape pod",  # "You're launched into space! Bye!"
            "giant electromagnet",  # "The giant electromagnet is stuck to you.  You can't move!!"
            "infinite loop",  # Literally halts the program in an infinite loop
            "molten lava",  # "The molten lava is way too hot! You melt!"
            "photons",  # "It is suddenly completely dark! You are eaten by a Grue!"

            "mug",  # Too heavy, by itself
            "prime number",  # Too heavy, by itself
            "weather machine",  # Too heavy, by itself

            "festive hat",  # Don't take this and our weight is correct with other items
        ]

    def part1(self):
        self.computer.reset()
        self.computer.run()

        back_moves: List[str] = []
        path_from_security: Optional[List[str]] = None
        seen: Set[Tuple[str, str]] = set()
        taken: Set[str] = set()

        while True:
            output = self.computer.output_str()
            # print(output)
            location = DungeonLocation.read(output)

            if location.name == "Security Checkpoint":
                path_from_security = back_moves.copy()
                previous_move = back_moves.pop()
                # print(f"Going back {previous_move}")
                self.computer.input_str(f"{previous_move}\n")
                continue

            for item in location.items:
                if item not in self._do_not_take:
                    taken.add(item)
                    input_str = f"take {item}\n"
                    # print(input_str)
                    self.computer.input_str(input_str)
                    response = self.computer.output_str()
                    # print(response)

            moved_through_a_door = False
            opposite_direction = None
            for direction in location.doors_here_lead:
                back_direction = back_moves[-1] if len(back_moves) > 0 else None
                if back_direction == direction:
                    continue

                movement = (location.name, direction)
                if movement in seen:
                    continue

                if direction == "north":
                    opposite_direction = "south"
                elif direction == "south":
                    opposite_direction = "north"
                elif direction == "east":
                    opposite_direction = "west"
                elif direction == "west":
                    opposite_direction = "east"

                seen.add(movement)
                back_moves.append(opposite_direction)
                moved_through_a_door = True

                # print(f"Going {direction}")
                self.computer.input_str(f"{direction}\n")

                break

            if not moved_through_a_door:
                if len(back_moves) > 0:
                    previous_move = back_moves.pop()
                    # print(f"Going back {previous_move}")
                    self.computer.input_str(f"{previous_move}\n")
                else:
                    break

        for movement in path_from_security:
            if movement == "north":
                movement = "south"
            elif movement == "south":
                movement = "north"
            elif movement == "east":
                movement = "west"
            elif movement == "west":
                movement = "east"

            self.computer.input_str(f"{movement}\n")
            self.computer.output_str()

        self.computer.input_str("east\n")
        output = self.computer.output_str()
        result = re.search(r"(\d+)", output).group(1)

        print("Part 1:", result)

    def part2(self):
        pass


if __name__ == '__main__':
    code = Y2019D25("2019/25.txt")
    code.part1()
    code.part2()
