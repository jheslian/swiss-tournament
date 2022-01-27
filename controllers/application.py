from operator import attrgetter
from models.matchs import Match
from models.tournament import Tournament
from models.players import Player
from models.rounds import Rounds
from views.base import View
from typing import List


class Application:
   tournaments = []

   def __init__(self, view):
      self.view = view
      self.current_tournament = None
      

   def controls(self, choice):
      control_list = {
         "t": self.view.prompt_for_tournament_menu(),
         "p": self.launch_tournament(),
      }
      if choice in control_list:
         return control_list[choice]

   

   def run(self):
      """ start application """
      main_menu = self.view.prompt_for_main_menu()
      self.controls(main_menu)



   def launch_tournament(self):
      content = self.view.prompt_create_tournament()
      self.get_tournament_details(content)
      players = self.get_players()
      self.tournament_rounds()
   

   
   def get_menu(self):
      """ unused """
      return self.view.prompt_for_main_menu()

      
   def get_tournament_details(self, content):
      """ create tournament """
      tournament = Tournament()
      tournament.name = content['name']
      tournament.location = content['location']
      tournament.tournament_date = content['tournament_date']
      tournament.time_type = content['time_type']
      tournament.description = content['description']
      self.current_tournament = tournament
      self.tournaments.append(self.current_tournament)
      return self.current_tournament


   def get_players(self):
      """Get some players."""
      while len(self.current_tournament.players) < self.current_tournament.no_of_players:
         content = self.view.prompt_for_player()
         if not content:
            return None
         player = Player()
         player.last_name = content['last_name']
         player.first_name = content['first_name']
         player.birthdate = content['birthdate']
         player.gender = content['gender']
         player.rank = content['rank']
         self.current_tournament.players.append(player)
      return self.current_tournament.players

   def tournament_rounds(self):
      while len(self.current_tournament.rounds) < self.current_tournament.no_of_rounds:
         round = Rounds(len(self.current_tournament.rounds) + 1)
         print("UU",round)
         

         # other pairs

         if str(round.name) == "Round 1":
            first_round_pairs = self.first_round_match_pairing()
            self.matches_per_round(first_round_pairs, round)
            round.list_of_match.append(first_round_pairs)
         else:
            other_rounds = self.other_round_match_pairing()
            self.matches_per_round(other_rounds, round)

      self.tournament_results()  

         
         
         #self.tournament.rounds.append(round)
      return self.current_tournament.rounds
   def tournament_results(self):
      return self.view.display_tournament_result(self.current_tournament.players)

   def matches_per_round(self, pairs, round):
      # print("**************$")
      # for i in self.tournament.players:
      #    print(i.score)
      # print("**************$")
      round_matches = {}
      match_list = []
      for pair in pairs:
         
         match = Match()   
         match.player1 = pair[0]
         match.player2 = pair[1]
         match_result = self.view.prompt_for_match_result(match.player1, match.player2)

         if match_result == None:
            match.player1.tmp_score = 0.5
            match.player2.tmp_score = 0.5
            match.player1.score += 0.5
            match.player2.score += 0.5
           
         if match_result ==  str(match.player1.last_name):
            match.player1.tmp_score = 1
            match.player1.score += 1         

         if match_result ==  str(match.player2.last_name): 
            match.player2.tmp_score = 1
            match.player2.score += 1     
               

         match_list.append(match)
         self.view.display_match_stats(match)
         
      round.list_of_match.append(match_list)   
      round_matches[str(round.name)] = match_list
      self.current_tournament.rounds.append(round_matches)   
      self.view.display_round_result(round_matches)



   def first_round_match_pairing(self):
      """ Match pairing for the first round and if score of all players are equal

      Sorts the list according to the player's rank and pair the first half to other half
      example: list = A, B, C, D, E, F, G, H 
               pair result = A vs E, B vs F, C vs G, D vs H 
      """
      player_list = self.current_tournament.players
      player_list.sort(key = attrgetter('rank'), reverse = True)
      
      if len(player_list) % 2 != 0:
         player_list.append(" ")
      split = int(len(player_list)/2)
      playerlist1 = player_list[:split]
      playerlist2 = player_list[split:]
      pairs = list(zip(playerlist1, playerlist2))
      return pairs

   def other_round_match_pairing(self):
      """ Match pairing for the other rounds

      Sorts the list according to the player's score and pair them with the total score almost or equally the same as them  
      example: list = A, B, C, D, E, F, G, H 
               pair result = A vs B, C vs D, E vs F, G vs H 
      """
      player_list = self.current_tournament.players
      player_list.sort(key = attrgetter('score'), reverse = True)
      
      if len(player_list) % 2 != 0:
         player_list.append(" ")
      pairs = list(zip(player_list[::2], player_list[1::2]))
      return pairs   

      
      
  