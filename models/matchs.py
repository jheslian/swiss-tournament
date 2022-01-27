""" Define game"""
from tkinter import S
from .players import Player
from typing import Tuple

class Match:
   def __init__(self, *args):
      self.player1: Tuple(*args)
      self.player2: Tuple(*args)

   def __str__(self):
      return self.player1.last_name

   def __repr__(self):
      """Used in print."""
      return self.player1.last_name + " " + self.player1.first_name + " vs " +  \
         self.player2.last_name + " " + self.player2.first_name


   # def player(self, player, score):
   #    return Tuple(Player(player), score)
         