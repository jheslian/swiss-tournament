""" Define game"""

from .players import Player
from typing import Tuple


class Match:
    def __init__(self, player1, player2):
        self.pair: Tuple[Player] = (player1, player2)

    def __str__(self):
        return str(self.pair[0]) + str(self.pair[1])

    def __repr__(self):
        return self.pair[0].last_name + " " + self.pair[0].first_name + " vs " + \
               self.pair[1].last_name + " " + self.pair[1].first_name
