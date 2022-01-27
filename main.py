""" Entry point. """


from sre_constants import GROUPREF_EXISTS
from models.tournament import Tournament
from controllers.application import Application
from views.base import View


def main():
   # tournament_name = input("Enter the name of the tournament: ")
   # no_of_players = int(input("How many players: "))
   # tournament = Tournament(no_of_players, tournament_name)
   # view = View()
   # controller = TournamentManager(tournament, view)
   # controller.launch_tournament()
   view = View()
   app = Application(view)
   app.run()
  
if __name__ == "__main__":
   main()