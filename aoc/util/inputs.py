from pathlib import Path
from typing import List

from aoc.util.grid import Grid


class Input(object):
    _input_dir = Path(__file__).parent.parent.parent / "inputs"

    def __init__(self, name):
        self.name = name

    @property
    def file_path(self):
        return self._input_dir / self.name

    def exists(self) -> bool:
        return self.file_path.exists()

    def touch(self):
        self.file_path.parent.mkdir(exist_ok=True, parents=True)
        self.file_path.touch(exist_ok=True)

    def line(self) -> str:
        with open(str(self.file_path), 'r') as fh:
            return fh.readline()

    def lines(self) -> List[str]:
        with open(str(self.file_path), 'r') as fh:
            return list(map(lambda line: line.rstrip('\n'), fh.readlines()))

    def ints(self) -> List[int]:
        return [int(x.strip()) for x in self.lines()]

    def int(self) -> int:
        return int(self.line())

    def int_line(self) -> List[int]:
        line = self.line()
        sep = ',' if ',' in line else ' '
        return [int(x) for x in line.split(sep)]

    def grouped(self):
        current_group = []
        groups = []
        for line in self.lines():
            if line == "":
                if len(current_group) > 0:
                    groups.append(current_group)
                    current_group = []
                continue
            current_group.append(line)

        groups.append(current_group)

        return groups

    def grid(self) -> Grid[str]:
        return Grid.from_str(self.lines())
