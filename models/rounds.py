""" Define rounds. """

from typing import List
from datetime import datetime
from models.matchs import Match

class Rounds():
   """Class for round of chess tournament."""
   def __init__(self, round_no, ):
      """ Initialize method """
      self.name = f"Round {round_no}"
      self.list_of_match: List[Match] = []
      self.start_datetime = self.start_datetime()
      self.end_datetime = None
   def __str__(self):
      return str(self.name)   

   def start_datetime(self):
      """ date and time when round is created """
      return datetime.now().strftime('%d-%m-Y, %H:%M:%S')  

   def end_datetime(self):
      """ date and time when round is terminated """
      return datetime.now().strftime('%d-%m-Y, %H:%M:%S')