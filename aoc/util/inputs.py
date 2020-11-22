from pathlib import Path


class Input(object):
    _input_dir = Path("/Users/jnesselr/PycharmProjects/AdventOfCode/inputs")

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

    def lines(self):
        with open(str(self.file_path), 'r') as fh:
            return list(map(lambda line: line.rstrip('\n'), fh.readlines()))

    def line(self):
        with open(str(self.file_path), 'r') as fh:
            return fh.readline()
