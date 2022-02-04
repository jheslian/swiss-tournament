""" Define view """

import sys
import pandas as pd
from tabulate import tabulate
import json


class View:

    # ===================================   MENU   ===================================#
    def prompt_for_main_menu(self):
        """ prompt for main menu. """
        print("\n==========   Menu   ==========")
        controls = [
            ["c", "Create a tournament"],
            ["p", "Play a tournament"],
            ["m", "Modify rank of a player"],
            ["lt", "List of tournaments"],
            ["lr", "List of rounds of a tournament"],
            ["lm", "List of matchs of a tournament"],
            ["lp", "List of players of a tournament"],
            ["ap", "List of all players sorted alphabetically"],
            ["rp", "List of all players sorted by ranks"],
            ["ur", "Update player rank"],
            ["q", "Quit"],
        ]
        print(tabulate(controls, headers=["controls", "description"]))
        choices = ['c', 'p', 'm', 'lt', 'lr', 'lm', 'lp', 'ap', 'rp', 'ur']
        answer = input("choice: ")
        if answer in choices:
            return answer
        elif answer == "q":
            return self.quit()
        else:
            print("option not found")
            return self.prompt_for_main_menu()

    @staticmethod
    def quit():
        """ Terminates the program """
        print("See you, bye!")
        sys.exit(0)

    # ===================================   TOURNAMENT   ===================================#
    @staticmethod
    def display_tournaments(tournaments):
        """ Display tournaments details """
        print("\n==========   List of tournaments   ==========\n")
        if tournaments:
            print(tabulate(tournaments, headers=["name", "location", "date", "time type", "description"]))
        else:
            print("\tList is empty")

    @staticmethod
    def prompt_create_tournament():
        """ Prompt for a tournament details """
        print("\n======   Add a tournament   ======")
        print("----------------------------------")
        name = input("Tournament name : ")
        location = input("Tournament location : ")
        tournament_date = input("Tournament date(mm-dd-yyy) : ")
        time_type = input("Tournament time type(bullet, blitz, rapid ) : ")
        description = input("Tournament description : ")
        details = {
            'name': name,
            'location': location,
            'tournament_date': tournament_date,
            'time_type': time_type,
            'description': description,
        }
        if not details:
            return None
        print(f"\nTournament created: ")
        for key, val in details.items():
            print(f"\t{key}: {val}")
        return details

    @staticmethod
    def prompt_tournament_id(title, tournaments):
        """ Get the tournament to play """
        print(f"\n======   {title}   ======")
        # print('r', tournaments, type(tournaments))
        if tournaments is None:
            return None

        print("Tournaments : ")
        res = []
        for val in tournaments:
            tmp = [val.doc_id, val['name']]
            res.append(tmp)

        print(tabulate(res, headers=["id", "name"]))
        data = input(f"\nEnter tournament id : ")
        if data is None:
            return None
        for tournament in res:
            if int(data) == tournament[0]:
                return tournament[0], tournament[1]
        return

    @staticmethod
    def display_tournament_result(players):
        """ Display the players withe the total score of the tournament """
        print("\n=====   Tournament results   =====")
        for player in players:
            print("Player:", player.last_name, player.first_name, " Score:", player.score)

    # ===================================   ROUND   ===================================#
    @staticmethod
    def display_round_result(round):
        """ Display players with the result of each round """
        for key, value in round.items():
            print(f"\n=======   {key}   =======")
            print("----------------------------")
            for val in value:
                print("Player:", val.pair[0].last_name, val.pair[0].first_name, " Score:", val.pair[0].tmp_score)
                print("Player:", val.pair[1].last_name, val.pair[1].first_name, " Score:", val.pair[1].tmp_score)

    @staticmethod
    def display_tournament_rounds(tournament_name, rounds):
        """ Display rounds of tournament"""
        print(f"\n=======    List of rounds for the tournament << {tournament_name} >>   =======")
        res = []
        for r in rounds:
            tmp = [r['name'], r['start_datetime'], r['end_datetime']]
            res.append(tmp)
        print(tabulate(res, headers=["name", "start date time", "end date time"]))

    # ===================================   MATCH   ===================================#
    @staticmethod
    def display_matches(matches):
        print(f"\n======   Matches   ======")
        for p in matches:
            print(
                f"{p[0].last_name} {p[0].first_name} {p[0].color} vs. {p[1].last_name} {p[1].first_name} {p[1].color}")

    def prompt_for_match_result(self, p1, p2):
        """ Prompt to get match result """
        print(f"\n======   Match : {p1.last_name} {p1.first_name} vs. {p2.last_name} {p2.first_name}  ======")
        option = [str(p1.last_name), str(p2.last_name)]
        result = input(f"Last name of the winner for this match(press ENTER for tie) : ")
        if not result:
            return None
        elif result not in option:
            print(f"player << {result} >> not found")
            return self.prompt_for_match_result(p1, p2)
        return result

    @staticmethod
    def display_match_stats(match):
        """ Display player with the score for the current match """
        print(f"\n======   Match : {match.pair[0].last_name}  vs. {match.pair[1].last_name}   ======")
        print("Player :", match.pair[0].last_name, match.pair[0].first_name, " Score: ", match.pair[0].tmp_score)
        print("Player :", match.pair[1].last_name, match.pair[1].first_name, " Score: ", match.pair[1].tmp_score)

    @staticmethod
    def display_tournament_matches(tournament_name, rounds):
        """ Display matches of a tournament"""
        print(f"\n=======    List of matches for the tournament << {tournament_name} >>   =======")
        content = {}
        for i in rounds:
            content[i['name']] = i['matches'][0]
        print(json.dumps(content, indent=4))

    # ===================================   PLAYER   ===================================#
    @staticmethod
    def get_player_name_update_rank():
        """ Get player name """
        print(f"\n======   Update player rank   ======")
        print("---------------------------------------")
        name = input("\nEnter player last name : ")
        if name is None:
            return None
        return name

    @staticmethod
    def get_player_id_rank_to_update(players):
        """ Get player id and rank """
        if players:
            print(tabulate(players, headers=["id", "last name", "first name", "birthdate", "gender", "score", "ranks"]))
        p_id = input("\nEnter player id to update : ")
        ids = []
        for p in players:
            print('loop', p[0])
            ids.append(p[0])
        if int(p_id) not in ids:
            print(f"Id << {p_id} >>  is not valid from selection")
            return None
        p_rank = input(f"Enter new rank of player {p_id} : ")
        print(f"Player {p_id} rank's has been changed to {p_rank}")
        return p_id, p_rank

    @staticmethod
    def prompt_for_player():
        """Prompt to add player."""
        print(f"\n======   Add a player   ======")
        print("---------------------------------------")
        last_name = input("Last name : ")
        first_name = input("First name : ")
        birthdate = input("Birthdate : ")
        gender = input("Gender : ")
        rank = input("Rank number : ")
        details = {
            'last_name': last_name,
            'first_name': first_name,
            'birthdate': birthdate,
            'gender': gender,
            'rank': rank
        }
        if not details:
            return None
        return details

    @staticmethod
    def display_sorted_players(title, players):
        """ Display all sorted players details from the tournaments"""
        print(f"\n==========   {title}   ==========")
        if players:
            print(tabulate(players, headers=["last name", "first name", "birthdate", "gender", "score", "ranks"]))
        else:
            print("\t\tList is empty")

    """@staticmethod
    def display_all_players_sorted_by_ranks(title, players):
       
        print(f"\n==========   {title}   ==========")
        if players:
            print(tabulate(players, reverse=True), headers=["last name", "first name", "ranks"])
        else:
            print("\t\tList is empty")"""

    def display_tournament_players(t_name, players):
        """ Display players of a tournament """
        print("\n==========   List of players by ranks   ==========")
