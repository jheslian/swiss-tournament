""" Define tournament """

from models.players import Player
from models.rounds import Rounds
from typing import List
from datetime import date 

class Tournament:
   # name = None
   # location = None
   # tournament_date: None
   # time_type: None
   # no_of_rounds: None

   def __init__(
      self, 
      name: str = None, 
      location: str = None, 
      tournament_date: str = None, 
      time_type: str = None, 
      no_of_rounds = 4
      ):
      
      self.name = str(name)
      self.location = str(location)
      self.tournament_date = tournament_date
      self.time_type = str(time_type)
      self.no_of_rounds = int(no_of_rounds)
      self.rounds : List(Rounds) = []
      self.players: List(Player) = []
      self.description = None
      self.no_of_players = 4

      
   def __str__(self):
      return self.name
         


   def __repr__(self):
      """Used in print."""
      return str(self)