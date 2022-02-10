""" Define controllers """

from operator import attrgetter
from models.matchs import Match
from models.tournament import Tournament
from models.players import Player
from models.rounds import Rounds
import database.tournaments.db_tournament as db_tournament
import database.players.db_players as db_player
import itertools
import random
import sys
import os


class Controller:
    """ Class that controls of the app """
    tournaments = []

    def __init__(self, view):
        self.view = view
        self.current_tournament = Tournament()

    def run(self):
        """ start application """

        try:
            while True:
                self.controls()
        except KeyboardInterrupt:
            print("\n\nProgram has been aborted! Data may have been lost, Goodbye!")
            sys.exit(0)

    # ===================================   CONTROLS   ===================================#
    @property
    def get_menu(self):
        """ Control menu

        Returns:
            str: chosen from the option
        """
        return self.view.prompt_for_main_menu()

    def controls(self):
        """ Controls of the app that calls the action to perform """
        choice = self.get_menu
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

    # ===================================   TOURNAMENT   ===================================#
    def create_tournament(self):
        """ Create a tournament """
        content = self.view.prompt_create_tournament()
        self.add_tournament(content)

    def launch_tournament(self):
        """ Play the tournament by adding the players and storing the result of each match """

        title = "Launch a tournament"
        tournament = self.view.prompt_tournament_id(title, db_tournament.get_tournaments_to_play())
        if tournament is None:
            return print("\tThere are no tournaments!")
        t_id = self.get_created_tournament(tournament[0])
        if t_id is None:
            return print("\tTournament not found!")
        if len(self.current_tournament.players) < self.current_tournament.no_of_players:
            self.get_players(int(t_id))
        if self.current_tournament.finished is False and self.current_tournament.playing is True:
            self.play_tournament(int(t_id))

    def get_created_tournament(self, t_id):
        """ Retrieve the tournament to play

        Args:
            t_id (int): choice of id from user input

        Returns:
            int: tournament id that match on the database
        """
        tournaments = db_tournament.get_tournaments_to_play()
        for val in tournaments:
            if t_id == val.doc_id:
                tournament = db_tournament.deserialize(val.doc_id)
                self.current_tournament = tournament
                db_tournament.start_playing(val.doc_id)
                return val.doc_id
        return None

    def get_all_tournaments(self):
        """ Retrieve all tournaments to display """
        result = db_tournament.get_tournaments()
        tournaments = []
        for res in result:
            val = [res['name'], res['location'], res['tournament_date'], res['time_type'], res['description']]
            tournaments.append(val)
        self.view.display_tournaments(tournaments)

    def play_tournament(self, t_id):
        """ Main part of tournament
        This generates the matches of the rounds and the result of the tournament or discontinue the tournament
        """
        while len(self.current_tournament.rounds) < self.current_tournament.no_of_rounds:
            round_no = len(self.current_tournament.rounds) + 1
            round = Rounds(round_no)
            q1 = "Would you like to start this round(y/n)? : "
            res = self.view.prompt_start_round(q1, round_no)
            if res is None:
                continue
            elif res.lower() != "y":
                q2 = "Are you sure you want to terminate the tournament(y/n)? : "
                confirm = self.view.prompt_start_round(q2, round_no)
                if confirm.lower() == "y":
                    print("Exit tournament! Goodbye!")
                    os.execv(sys.executable, ['python'] + sys.argv)

            round.start()

            if str(round.name) == "Round 1":
                """ generate pair for the first round """
                first_round_pairs = self.first_round_match_pairing()
                self.get_score_of_matches_per_round(first_round_pairs, round)
                round.list_of_match.append(first_round_pairs)

            else:
                """ generate pair for the other rounds """
                other_rounds = self.other_round_match_pairing()
                self.get_score_of_matches_per_round(other_rounds, round)
                round.list_of_match.append(other_rounds)
            round.terminate()
            self.current_tournament.rounds.append(round)
            db_tournament.update_rounds(t_id, round)
        self.tournament_results()
        db_tournament.ended(t_id)
        return self.current_tournament.rounds

    def add_tournament(self, content):
        """ Create a tournament

        Args:
            content (dict): details from user input

        Returns:
            tournament obj: object created
        """
        tournament = Tournament()
        tournament.name = content['name']
        tournament.location = content['location']
        tournament.tournament_date = content['tournament_date']
        tournament.time_type = content['time_type']
        tournament.description = content['description']
        if content['no_of_players']:
            tournament.no_of_players = content['no_of_players']
        if content['no_of_rounds']:
            tournament.no_of_rounds = content['no_of_rounds']
        self.current_tournament = tournament
        db_tournament.save(tournament)
        return self.current_tournament

    def tournament_results(self):
        """ Results of the tournament to display """
        results = self.current_tournament.players
        return self.view.display_tournament_result(results)

    # ===================================   PLAYERS   ===================================#
    def get_players(self, t_id):
        """ Add players to play a tournament

        Args:
            t_id (int): id of the tournament to play

        Returns:
            list: players to be added to the tournament
        """
        while len(self.current_tournament.players_ids) < self.current_tournament.no_of_players:
            res = self.view.prompt_for_player()
            if not res:
                return None
            player = Player(res['last_name'], res['first_name'], res['birthdate'], res['gender'], res['rank'])
            player_id = db_player.save(player)
            player.id = player_id
            self.current_tournament.players_ids.append(player_id)
            self.current_tournament.players.append(player)
        db_tournament.add_players_id(t_id, self.current_tournament.players_ids)
        return self.current_tournament.players

    def get_all_players_sorted_by_alphabet(self):
        """ Retrieve data of all players in all tournaments, convert to list and sort it to use it in tabular form """
        sorted_players = self.get_all_players(db_player.get_players())
        sorted_players.sort()
        title = "List of players by alphabet"
        self.view.display_sorted_players(title, sorted_players)

    def get_all_players_sorted_by_ranks(self):
        """ Retrieve data of all players in all tournaments, convert to list and sort it to use it in tabular form  """
        sorted_players = self.get_all_players(db_player.get_players())
        sorted_players.sort(key=lambda sorted_players: sorted_players[5], reverse=True)
        title = "List of players by ranks"
        self.view.display_sorted_players(title, sorted_players)

    def get_player_to_update(self):
        """ Display certain players that match the name of the desired played and
        retrieve the player to update the rank """
        p_name = self.view.get_player_name()
        if p_name is None:
            return None

        result_players = db_player.search_player(p_name)
        if result_players is None:
            return print("\tPlayer not found")
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
        """ Retrieve and display players of a tournament in alphabetically and sorted by ranks  """
        try:
            title = "Search tournament"
            tournament = self.view.prompt_tournament_id(title, db_tournament.get_tournaments())
        except ValueError:
            return print("\tInput is not a digit!")

        if tournament is None:
            return print("\tNo tournaments found!")

        res = db_tournament.get_players(tournament[0])
        if res is None:
            return print("\tThis tournament is not yet played!")
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
        """ Generate matches from the pairing, get the winner of the match and
        display the result at the end of each match  """
        round_matches = {}
        match_list = []
        self.view.display_matches(pairs)
        for pair in pairs:
            match = Match(pair[0], pair[1])
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
            db_player.update_score(match.pair[0])
            db_player.update_score(match.pair[1])
            self.view.display_match_stats(match)

        round_matches[str(round.name)] = match_list
        self.view.display_round_result(round_matches)

    def get_tournament_rounds(self):
        """ Retrieve tournament rounds """
        try:
            title = "Search tournament"
            tournament = self.view.prompt_tournament_id(title, db_tournament.get_tournaments())
        except ValueError:
            return print("\tInput is not a digit!")
        if tournament is None:
            return print("\tNo tournaments found!")

        res = db_tournament.get_rounds(tournament[0])
        self.view.display_tournament_rounds(tournament[1], res)

    # ===================================   MATCH   ===================================#
    def get_tournament_matches(self):
        """ Retrieve tournament rounds """
        try:
            title = "Search tournament"
            tournament = self.view.prompt_tournament_id(title, db_tournament.get_tournaments())
        except ValueError:
            return print("\tInput is not a digit!")

        if tournament is None:
            return print("\tNo tournaments found!")

        res = db_tournament.get_rounds(tournament[0])
        if res is None:
            return print("\tThis tournament is not yet played!")
        self.view.display_tournament_matches(tournament[1], res)

    def first_round_match_pairing(self):
        """ Match pairing for the first round and if score of all players are equal

        Sorts the list according to the player's rank and pair the first half to other half
        example: list = A, B, C, D, E, F, G, H
               pair result = A vs E, B vs F, C vs G, D vs H

        Returns:
            list: pairs of match generated to play ont the next round

        """
        player_list = self.current_tournament.players
        player_list.sort(key=attrgetter('rank'), reverse=True)

        if len(player_list) % 2 != 0:
            player_list.append(" ")
        split = int(len(player_list) / 2)
        playerlist1 = player_list[:split]
        playerlist2 = player_list[split:]
        new_pairs = list(zip(playerlist1, playerlist2))
        self.player_color_generator(new_pairs)
        return new_pairs

    def other_round_match_pairing(self):
        """ Match pairing for the other rounds

        Sorts the list according to the player's score or by ranks and pair them with the total
        score almost or equally the same as them
        example: list = A, B, C, D, E, F, G, H
               pair result = A vs B, C vs D, E vs F, G vs H

        Returns:
            list: pairs of match generated to play ont the next round
        """
        players = db_player.get_match_players(self.current_tournament.players_ids)
        tie = False
        scores = []
        for player in players:
            if len(scores) > 0 and player['tmp_score'] in scores:
                tie = True
                break
            scores.append(player['tmp_score'])
        player_list = self.current_tournament.players
        player_list.sort(key=attrgetter('score'), reverse=True)
        if tie is True:
            player_list.sort(key=attrgetter('rank'), reverse=True)

        new_pairs = []
        paired_players = []
        players_with_pair = []
        for i, player in enumerate(player_list):
            for j, pair in enumerate(itertools.combinations(player_list, 2)):
                if pair[1] not in pair[0].played_with and pair[0] not in pair[1].played_with and player == pair[0] \
                        and pair not in paired_players and pair[0] not in players_with_pair and pair[1] \
                        not in players_with_pair:
                    paired_players.append(pair)
                    new_pairs.append(pair)
                    players_with_pair.append(pair[0])
                    players_with_pair.append(pair[1])
        self.player_color_generator(new_pairs)
        return new_pairs

    # ===================================   STATIC METHODS   ===================================#
    @staticmethod
    def player_color_generator(pairs):
        """ Generates player's color for the match

        Args:
            pairs (list): pair of players for the matches of a round

        Returns:
            list: pair of player with their color for the match
        """
        for pair in pairs:
            res = random.choice(["WHITE", "BLACK"])
            pair[0].color = res
            if res == "WHITE":
                pair[1].color = "BLACK"
            else:
                pair[1].color = "WHITE"
        return pairs

    @staticmethod
    def get_all_players(players_dict):
        """ Retrieve all players and converts to list to display

        Args:
            players_dict (dict): players in a dictionnary to convert

        Returns:
            list: converted list of players
        """
        players = []
        for player in players_dict:
            tmp = [player['last_name'], player['first_name'], player['birth_date'],
                   player['gender'], player['score'], player['rank']]
            players.append(tmp)
        return players

    @staticmethod
    def tournament_rounds(t_id):
        """ Retrieve rounds of a tournament

        Args:
            t_id (int): id of a tournament to retrieve

        Returns:
            round obj: details of the rounds
        """
        rounds = []
        tournament = db_tournament.get_rounds(t_id)
        for r in tournament:
            tmp = [r['name'], r['start_datetime'], r['end_datetime']]
            rounds.append(tmp)
        return rounds
