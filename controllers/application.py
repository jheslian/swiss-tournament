""" Define application """

from operator import attrgetter
from models.matchs import Match
from models.tournament import Tournament
from models.players import Player
from models.rounds import Rounds
import database.tournaments.db_tournament as db_tournament
import database.players.db_players as db_player
import itertools
import random


class Application:
    tournaments = []

    def __init__(self, view):
        self.view = view
        self.current_tournament = Tournament()

    def run(self):
        """ start application """
        while True:
            self.controls()

    def controls(self):
        choice = self.get_menu()
        control_list = {
            "c": self.create_tournament,
            "p": self.launch_tournament,
            "lt": self.get_all_tournaments,
            "lr": self.get_tournament_rounds,
            'lm': self.get_tournament_matches,
            'lp': self.get_tournament_players,
            "ap": self.get_all_players_sorted_by_alphabet,
            "rp": self.get_all_players_sorted_by_ranks,
            "ur": self.get_player_to_update,
        }
        control_list[choice]()

    # ===================================   CONTROLS   ===================================#
    def get_menu(self):
        """ Control menu """
        return self.view.prompt_for_main_menu()

    # ===================================   TOURNAMENT   ===================================#
    def create_tournament(self):
        """ Create a tournament """
        content = self.view.prompt_create_tournament()
        self.add_tournament(content)

    def launch_tournament(self):
        """ Play the tournament """
        title = "Launch a tournament"
        tournament = self.view.prompt_tournament_id(title, db_tournament.get_tournaments_to_play())
        if tournament is None:
            return print(f"\tThere are no tournaments!")
        res = self.get_created_tournament(tournament)
        print('rrr', res)
        if res is None:
            return print(f"\tTournament not found!")
        db_tournament.start_playing(int(res))
        self.get_players()
        self.play_tournament()

    def get_created_tournament(self, choice):
        """ Retrieve tournament to play"""
        tournaments = db_tournament.get_tournaments_to_play()
        print("crea", choice, type(choice))
        for val in tournaments:

            if choice == val.doc_id:

                self.current_tournament.name = val["name"]
                self.current_tournament.location = val["location"]
                self.current_tournament.tournament_date = val["tournament_date"]
                self.current_tournament.description = val["description"]
                self.current_tournament.no_of_rounds = val["no_of_rounds"]
                self.current_tournament.playing = True
                return val.doc_id
        return None

    def get_all_tournaments(self):
        """ Retrieve all tournaments """
        result = db_tournament.get_tournaments()
        tournaments = []
        for res in result:
            val = [res['name'], res['location'], res['tournament_date'], res['time_type'], res['description']]
            tournaments.append(val)
        self.view.display_tournaments(tournaments)

    def play_tournament(self):
        """ Main part of tournament
      
      This generates the matches of the rounds and the result of the tournament
      """

        while len(self.current_tournament.rounds) < self.current_tournament.no_of_rounds:
            round = Rounds(len(self.current_tournament.rounds) + 1)

            """ res = self.view.get_start_round()
            if res.lower() != "y":
                return None"""
            round.start_round()
            print("start time",round.start_datetime)

            if str(round.name) == "Round 1":
                """ generate pair for the first round"""
                first_round_pairs = self.first_round_match_pairing()
                self.get_score_of_matches_per_round(first_round_pairs, round)
                print("ret", first_round_pairs)
                round.list_of_match.append(first_round_pairs)
            else:
                """ generate pair for the other rounds"""
                other_rounds = self.other_round_match_pairing()
                self.get_score_of_matches_per_round(other_rounds, round)
                print("ret2", first_round_pairs)
                round.list_of_match.append(other_rounds)
            round.end_round()
            self.current_tournament.rounds.append(round)
            print("endtime", round.end_datetime)
            print("play tournament", round.list_of_match)
        self.tournament_results()

        return self.current_tournament.rounds

    def add_tournament(self, content):
        """ create tournament """
        tournament = Tournament()
        tournament.name = content['name']
        tournament.location = content['location']
        tournament.tournament_date = content['tournament_date']
        tournament.time_type = content['time_type']
        tournament.description = content['description']
        self.current_tournament = tournament
        self.tournaments.append(self.current_tournament)
        db_tournament.save(tournament)
        return self.current_tournament

    def tournament_results(self):
        """ Results of the tournament """
        results = self.current_tournament.players
        print("ending")
        for player in results:
            print("score", player.score)
            db_player.update_score(player)
        db_tournament.update_rounds(self.current_tournament)
        return self.view.display_tournament_result(results)

    # ===================================   PLAYERS   ===================================#
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
            player_id = db_player.save(player)
            player.id = player_id
            self.current_tournament.players_ids.append(player_id)
            self.current_tournament.players.append(player)
        db_tournament.add_players_id(self.current_tournament)
        return self.current_tournament.players

    def get_all_players_sorted_by_alphabet(self):
        """ Retrieve data of all players in all tournaments, convert to list and sort it to use it in tabular form  """
        sorted_players = self.get_all_players(db_player.get_players())
        sorted_players.sort()
        title = "List of players by alphabet"
        return self.view.display_sorted_players(title, sorted_players)

    def get_all_players_sorted_by_ranks(self):
        """ Retrieve data of all players in all tournaments, convert to list and sort it to use it in tabular form  """
        sorted_players = self.get_all_players(db_player.get_players())
        sorted_players.sort(key=lambda sorted_players: sorted_players[5], reverse=True)
        title = "List of players by ranks"
        return self.view.display_sorted_players(title, sorted_players)

    def get_player_to_update(self):
        p_name = self.view.get_player_name_update_rank()
        if p_name is None:
            return None
        print("searching for", p_name)

        result_players = db_player.search_player(p_name)
        print("res", result_players)
        players = []
        for player in result_players:
            tmp = [player.doc_id, player['last_name'], player['first_name'], player['birth_date'],
                   player['gender'], player['score'], player['rank']]
            players.append(tmp)

        res = self.view.get_player_id_rank_to_update(players)
        if res is None:
            return None
        db_player.update_rank(res[0], res[1])

    def get_tournament_players(self):
        """ Retrieve/display players of a tournament """
        try:
            title = "Search tournament"
            tournament = self.view.prompt_tournament_id(title, db_tournament.get_tournaments())
        except ValueError:
            return print(f"\tInput is not a digit!")

        if tournament is None:
            return print(f"\tNo tournaments found!")

        res = db_tournament.get_players(tournament[0])
        if res is None:
            return print(f"\tThis tournament is not yet played!")
        players = db_player.get_match_players(res)

        # sorted by alphabet
        title1 = f"Tournament {tournament[1]} :  List of player sorted by alphabet"
        players_by_alphabet = self.get_all_players(players)
        players_by_alphabet.sort()
        self.view.display_sorted_players(title1, players_by_alphabet)

        # sorted by ranks
        title2 = f"Tournament {tournament[1]} :  List of player sorted by ranks"
        players_by_alphabet.sort(key=lambda sorted_players: sorted_players[5], reverse=True)
        self.view.display_sorted_players(title2, players_by_alphabet)

    # ===================================   ROUND   ===================================#
    def get_score_of_matches_per_round(self, pairs, round):
        """ Generate matches from the pairing, get the scores and display the result at the end of each match  """
        round_matches = {}
        match_list = []
        self.view.display_matches(pairs)
        for pair in pairs:
            match = Match(pair[0], pair[1])

            print("222zz", match)
            match.pair[0].played_with.append(pair[1])
            match.pair[1].played_with.append(pair[0])
            match.pair[0].tmp_score = 0
            match.pair[1].tmp_score = 0
            match_result = self.view.prompt_for_match_result(match.pair[0], match.pair[1])

            """ Score: 
             winner: 1
             tie: 0.5 """
            if match_result is None:
                match.pair[0].tmp_score = 0.5
                match.pair[1].tmp_score = 0.5
                match.pair[0].score += 0.5
                match.pair[1].score += 0.5
            if match_result == str(match.pair[0].last_name):
                match.pair[0].tmp_score = 1
                match.pair[1].score += 1
            if match_result == str(match.pair[1].last_name):
                match.pair[0].tmp_score = 1
                match.pair[1].score += 1
            match_list.append(match)
            self.view.display_match_stats(match)

        round_matches[str(round.name)] = match_list
        self.view.display_round_result(round_matches)

    def get_tournament_rounds(self):
        """ Retrieve tournament rounds """
        try:
            title = "Search tournament"
            tournament = self.view.prompt_tournament_id(title, db_tournament.get_tournaments())
        except ValueError:
            return print(f"\tInput is not a digit!")
        if tournament is None:
            return print(f"\tNo tournaments found!")

        res = db_tournament.get_rounds(tournament[0])
        self.view.display_tournament_rounds(tournament[1], res)

    # ===================================   MATCH   ===================================#
    def get_tournament_matches(self):
        """ Retrieve tournament rounds """
        try:
            title = "Search tournament"
            tournament = self.view.prompt_tournament_id(title, db_tournament.get_tournaments())
        except ValueError:
            return print(f"\tInput is not a digit!")

        if tournament is None:
            return print(f"\tNo tournaments found!")

        res = db_tournament.get_rounds(tournament[0])
        if res is None:
            return print(f"\tThis tournament is not yet played!")
        self.view.display_tournament_matches(tournament[1], res)

    def first_round_match_pairing(self):
        """ Match pairing for the first round and if score of all players are equal

      Sorts the list according to the player's rank and pair the first half to other half
      example: list = A, B, C, D, E, F, G, H 
               pair result = A vs E, B vs F, C vs G, D vs H 
      """
        player_list = self.current_tournament.players
        player_list.sort(key=attrgetter('rank'), reverse=True)

        if len(player_list) % 2 != 0:
            player_list.append(" ")
        split = int(len(player_list) / 2)
        playerlist1 = player_list[:split]
        playerlist2 = player_list[split:]
        pairs = list(zip(playerlist1, playerlist2))
        self.player_color_generator(pairs)
        print("1st match", pairs)
        return pairs

    def other_round_match_pairing(self):
        """ Match pairing for the other rounds

      Sorts the list according to the player's score and pair them with the total
      score almost or equally the same as them
      example: list = A, B, C, D, E, F, G, H
           pair result = A vs B, C vs D, E vs F, G vs H
      """
        player_list = self.current_tournament.players
        player_list.sort(key=attrgetter('score'), reverse=True)
        if len(player_list) % 2 != 0:
            player_list.append(" ")

        new_pairs = []
        players_with_pair = []
        for i, player in enumerate(player_list):
            for j, pair in enumerate(itertools.combinations(player_list, 2)):
                if j == 0 and i == 0:
                    players_with_pair.append(pair[0])
                    players_with_pair.append(pair[1])
                    new_pairs.append(pair)
                else:
                    if pair[1] not in pair[0].played_with and pair[0] not in pair[1].played_with and player == pair[0] \
                            and pair[0] not in players_with_pair and pair[1] not in players_with_pair:
                        players_with_pair.append(pair[0])
                        players_with_pair.append(pair[1])
                        new_pairs.append(pair)
                j += 1
            i += 1
        self.player_color_generator(new_pairs)
        print("other pair", new_pairs)
        return new_pairs

    # ===================================   STATIC METHODS   ===================================#
    @staticmethod
    def player_color_generator(pairs):
        """ Player's color """
        for pair in pairs:
            print("in", pair)
            res = random.choice(["WHITE", "BLACK"])
            pair[0].color = res
            if res == "WHITE":
                pair[1].color = "BLACK"
            else:
                pair[1].color = "WHITE"
        return pairs

    @staticmethod
    def get_all_players(players_dict):
        print("DICT", players_dict)
        """ Retrieve all players"""
        players = []
        for player in players_dict:
            tmp = [player['last_name'], player['first_name'], player['birth_date'],
                   player['gender'], player['score'], player['rank']]
            players.append(tmp)

        return players

    @staticmethod
    def tournament_rounds(t_id):
        """ Retrieve rounds of a tournament   """
        rounds = []
        tournament = db_tournament.get_rounds(t_id)
        for r in tournament:
            tmp = [r['name'], r['start_datetime'], r['end_datetime']]
            rounds.append(tmp)
        return rounds

    @staticmethod
    def tournament_matches():
        pass
