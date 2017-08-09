class TicTacToeGrid:
    GRID_LENGTH = 3

    def __init__(self):
        self.spots = [[None for x in range(self.GRID_LENGTH)] for y in range(self.GRID_LENGTH)]
        self.finished = False
        self.won = False
        self.winner_token = None

    def is_position_empty(self, row, col):
        return self.spots[row][col] is None

    def set_position(self, row, col, token):
        self.spots[row][col] = token
        if token is None:
            self.finished = False
            self.won = False
            self.winner_token = None
        else:
            self._check_for_winner()
            if not self.finished:
                self._check_is_finished()

    def _check_for_winner(self):
        winner_patterns = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]
        for pattern in winner_patterns:
            winner = True
            token = None
            for position in pattern:
                token_at_spot = self.spots[position[0]][position[1]]
                if token_at_spot is None:
                    winner = False
                    break
                if token is None:
                    token = token_at_spot
                elif token != token_at_spot:
                    winner = False
                    break

            if winner:
                self.finished = True
                self.won = True
                self.winner_token = self.spots[position[0]][position[1]]

    def _check_is_finished(self):
        for col in self.spots:
            for spot in col:
                if spot is None:
                    return

        self.finished = True

    def total_spaces(self):
        return len(self.spots) * len(self.spots[0])

    def empty_spots(self):
        empty_spots = []
        for y in range(len(self.spots)):
            for x in range(len(self.spots[0])):
                if self.spots[y][x] is None:
                    empty_spots.append((y, x))
        return empty_spots

    def __str__(self):
        output = []
        output.append("  1 2 3\n")
        for (y, row) in enumerate(self.spots):
            if y > 0:
                output.append("  -+-+-\n")
            output.append(str(y + 1) + " ")
            for x, spot in enumerate(row):
                if x > 0:
                    output.append("|")

                if spot is None:
                    spot_str = " "
                else:
                    spot_str = spot
                output.append(spot_str)
            output.append("\n")
        return ''.join(output).encode('utf-8')
