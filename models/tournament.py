""" Define tournament """

from models.players import Player
from models.rounds import Rounds
from typing import List


class Tournament:
    def __init__(
            self,
            name: str = None,
            location: str = None,
            tournament_date: str = None,
            time_type: str = None,
            no_of_rounds=4
    ):
        self.name = str(name)
        self.location = str(location)
        self.tournament_date = str(tournament_date)
        self.time_type = str(time_type)
        self.no_of_rounds = int(no_of_rounds)
        self.rounds: List[Rounds] = []
        self.players: List[Player] = []
        self.players_ids = []
        self.description = None
        self.no_of_players = 8
        self.playing = False


    def __str__(self):
        """ Str print """
        return self.name

    def __repr__(self):
        """Used in print."""
        return str(self)

