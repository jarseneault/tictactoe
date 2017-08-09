import abc
import random
import sys

if sys.version_info[0] <= 2:
    range = xrange
    input = raw_input

class TicTacToePlayer:
    __metaclass__ = abc.ABCMeta

    def __init__(self, token):
        self.token = token

    @abc.abstractmethod
    def take_turn(self, grid):
        raise NotImplementedError("Players must have a take_turn method implemented")

class HumanPlayer(TicTacToePlayer):
    def take_turn(self, grid):
        valid = range(1, grid.GRID_LENGTH + 1)
        grid_position_empty = False

        while not grid_position_empty:
            while True:
                try:
                    col = int(input("Which column: "))
                    if col in valid:
                        col -= 1
                        break
                except ValueError:
                    print("Invalid column, try again.\n")
            while True:
                try:
                    row = int(input("Which row: "))
                    if row in valid:
                        row -= 1
                        break
                except ValueError:
                    print("Invalid row, try again.\n")

            grid_position_empty = grid.is_position_empty(row, col)
            if not grid_position_empty:
                print("Position already filled, try again.\n")

        grid.set_position(row, col, self.token)

class ComputerPlayer(TicTacToePlayer):
    def take_turn(self, grid):
        print("Thinking...\n")
        self.current_choice = None
        self.active_turn = self.token
        move = self._determine_best_move(grid, self.token)
        grid.set_position(move[0], move[1], self.token)

    def _determine_best_move(self, grid, token):
        best = -15
        potentials = []

        possible_moves = self._get_possible_moves(grid)

        if len(possible_moves) == grid.total_spaces():
            return random.choice(possible_moves)

        for move in possible_moves:
            grid.set_position(move[0], move[1], self.token)
            #score = self._minimax(grid, self._get_opposite_token(self.token))
            score = -self._alphabeta(grid, self._get_opposite_token(token), -15, 15)
            grid.set_position(move[0], move[1], None)
            if score > best:
                best = score
                potentials = [move]
            elif score == best:
                potentials.append(move)

        if best == 10:
            print("Gotcha.\n")
        return random.choice(potentials)

    def _minimax(self, grid, token):
        if grid.finished:
            return self._score(grid)

        best = None

        possible_moves = self._get_possible_moves(grid)
        for move in possible_moves:
            grid.set_position(move[0], move[1], token)
            score = self._minimax(grid, self._get_opposite_token(token))
            grid.set_position(move[0], move[1], None)

            if token == self.token:
                if best is None or score > best:
                    best = score
            else:
                if best is None or score < best:
                    best = score
        return best

    def _alphabeta(self, grid, token, alpha, beta):
        if token == self.token:
            sign = 1
        else:
            sign = -1

        if grid.finished:
            return sign * self._score(grid)

        score = -15
        best = None

        possible_moves = self._get_possible_moves(grid)
        for move in possible_moves:
            grid.set_position(move[0], move[1], token)
            score = -self._alphabeta(grid, self._get_opposite_token(token), -beta, -alpha)
            grid.set_position(move[0], move[1], None)
            if best is None or best < score:
                best = score

            alpha = max(alpha, score)
            if alpha >= beta:
                break

        return best

    def _get_possible_moves(self, grid):
        return grid.empty_spots()

    def _score(self, grid):
        if grid.finished:
            if grid.won:
                if grid.winner_token == self.token:
                    return 10
                else:
                    return -10
            else:
                return 0
        else:
            raise GridNotFinishedError

    def _get_opposite_token(self, token):
        if token == "X":
            return "O"
        return "X"

class GridNotFinishedError(Exception):
    pass
