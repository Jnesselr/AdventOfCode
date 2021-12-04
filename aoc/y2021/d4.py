from typing import List, Set

from aoc.util.inputs import Input


class BingoBoard(object):
    def __init__(self, group: List[str]):
        self._marked: Set[int] = set()
        self._board: List[List[int]] = []

        for line in group:
            while '  ' in line:
                line = line.replace('  ', ' ')
            self._board.append([int(x.lstrip(' ')) for x in line.strip(' ').split(' ')])

    def mark(self, item: int):
        self._marked.add(item)

    def reset(self):
        self._marked = set()

    def unmarked(self) -> Set:
        result = set()

        for row in self._board:
            for item in row:
                if item not in self._marked:
                    result.add(item)

        return result

    @property
    def winner(self) -> bool:
        for row_num in range(5):
            if self._board[row_num][0] in self._marked and \
                    self._board[row_num][1] in self._marked and \
                    self._board[row_num][2] in self._marked and \
                    self._board[row_num][3] in self._marked and \
                    self._board[row_num][4] in self._marked:
                return True

        for col_num in range(5):
            if self._board[0][col_num] in self._marked and \
                    self._board[1][col_num] in self._marked and \
                    self._board[2][col_num] in self._marked and \
                    self._board[3][col_num] in self._marked and \
                    self._board[4][col_num] in self._marked:
                return True

        return False


class Y2021D4(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()

        self.choices: List[int] = [int(x) for x in groups[0][0].split(',')]
        self.boards: List[BingoBoard] = [BingoBoard(group) for group in groups[1:]]

    def part1(self):
        result = 0

        for board in self.boards:
            board.reset()

        for choice in self.choices:
            for board in self.boards:
                board.mark(choice)

                if board.winner:
                    result = sum(board.unmarked()) * choice
                    break
            if result != 0:
                break

        print("Part 1:", result)

    def part2(self):
        for board in self.boards:
            board.reset()

        already_won = set()
        last_winning_board = None
        last_winning_choice = None

        for choice in self.choices:
            for index, board in enumerate(self.boards):
                if index in already_won:
                    continue
                board.mark(choice)

                if board.winner:
                    last_winning_board = board
                    last_winning_choice = choice
                    already_won.add(index)

        result = sum(last_winning_board.unmarked()) * last_winning_choice

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D4("2021/4.txt")
    code.part1()
    code.part2()
