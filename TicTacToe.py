#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import sys
import random

from Grid import TicTacToeGrid
from Players import HumanPlayer, ComputerPlayer

if sys.version_info[0] <= 2:
    range = xrange
    input = raw_input

class TicTacToe:
    def __init__(self):
        self.grid = TicTacToeGrid()
        valid = ['Y', 'N']
        try:
            while True:
                start_first = str(input("Start first (Y/N)? X goes first: ")).upper()
                if(start_first in valid):
                    break
        except ValueError:
            pass
        except KeyboardInterrupt:
            print("\nCtrl-C detected, exiting.\n")
            sys.exit()

        if start_first == 'Y':
            self.players = [HumanPlayer('X'), ComputerPlayer('O')]
        else:
            self.players = [ComputerPlayer('X'), HumanPlayer('O')]

    def game_loop(self):
        try:
            player_idx = 1
            player = None
            while not self.grid.finished:
                print(self.grid)
                player_idx += 1
                player_idx %= len(self.players)
                player = self.players[player_idx]
                player.take_turn(self.grid)

            print(self.grid)
            if self.grid.won:
                won = isinstance(player, HumanPlayer)
                if won:
                    print("You Won!\n")
                else:
                    print("You lost.\n")
            else:
                print("It's a draw.\n")
        except KeyboardInterrupt:
            print("\nCtrl-C detected, exiting.\n")

if __name__ == "__main__":
    game = TicTacToe()
    game.game_loop()
