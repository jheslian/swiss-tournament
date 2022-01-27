""" Define player. """
import uuid
#from database.database import insert_player 

class Player:
   def __init__(self, last_name: str = None, first_name: str = None, 
               birthdate: str = None, gender: str = None, rank = 0):
      self.last_name = last_name
      self.first_name = first_name
      self.birthdate = birthdate
      self.gender = gender
      self.rank = int(rank)
      self.score = 0
      self.tmp_score = 0

   def __str__(self):
      return self.last_name

   def __repr__(self):
      """Used in print."""
      return str(self)   

   def update_rank(self, rank):
      """ update player rank """
      self.rank = rank
      return self.rank  

   def is_bye(self):
      return self.score + 1

   def save_player_in_database(self):
      serialized_players = {
         'name': self.name, 
         'score': self.current_score,
         'pair_with': self.pair_with
      }
      #insert_player(serialized_players)

   def get_players_in_database(self):
      pass


