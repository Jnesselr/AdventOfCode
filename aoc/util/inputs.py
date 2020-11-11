from pathlib import Path

_input_dir = Path("/Users/jnesselr/PycharmProjects/AdventOfCode/inputs")


def touch(name):
    file_path = (_input_dir / name)
    file_path.parent.mkdir(exist_ok=True, parents=True)
    file_path.touch(exist_ok=True)


def input_list(name):
    file_path = (_input_dir / name)
    with open(str(file_path), 'r') as fh:
        return list(fh.readlines())
