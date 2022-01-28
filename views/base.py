""" Define view """

import sys
from tabulate import tabulate
class View:
    def prompt_for_main_menu(self):
        """ prompt for main menu. """
        print("\n==========   Menu   ==========")
        controls = [
            ["p", "Play a tournament"],
            ["m", "Modify rank of a player"],
            ["lt", "List of tournaments"],
            ["ap", " List of all players sorted alphabetically"],
            ["rp", "List of all players sorted by ranks"],
            ["q", "Quit"],
        ]
        print(tabulate(controls, headers=["controls", "description"]))
        choices = ['p', 'm', 'lt', 'ap', 'rp' ]    
        answer = input("choice: ")
        if answer in choices:
            return answer
        elif answer == "q": 
            return self.quit()
        else: 
            print("option not found")
            return self.prompt_for_main_menu()

        
    def modify_player_rank(self, name):
        """ Modify player rank. """
        pass


    # def display_list_of_tournaments(self, tournaments):
    #     print(
    #         "======   List of tournaments   ======\
    #          -------------------------------------"
    #         )
    #     for tournament in tournaments:
    #         print(tournament)
        
    #     answer = input("Enter the name tournament to consult, or enter any keys to return to Tournament menu")
    #     if answer in tournaments:
    #         return self.prompt_for_specific_tournament(answer)
    #     else:
    #         return self.prompt_for_tournament_menu() 
    

    def quit(self):
        """ Terminates the program """
        print("See you, bye!")
        sys.exit(0)     


    def prompt_create_tournament(self):
        """ Prompt for a tournament details """
        print("\n======   Add a tournament   ======")
        print("----------------------------------")
        name = input("Tournament name : ")
        location = input("Tournament location : ")
        tournament_date = input("Tournament date : ")
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
        return details


    def prompt_for_player(self):
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


    def display_match_stats(self, match):
        """ Display player with the score for the current match """
        print(f"\n======   Match : {match.player1.last_name}  vs. {match.player2.last_name}   ======")
        print("Player: ",match.player1.last_name, match.player1.first_name, " Score: ", match.player1.tmp_score)
        print("Player: ",match.player2.last_name, match.player2.first_name, " Score: ", match.player2.tmp_score)
        

    def display_round_result(self, round):
        """ Display players with the result of each round """
        for key, value in round.items() :
            print (f"\n=======   {key}   =======")
            print("----------------------------")
            for val in value:
                print("Player:",val.player1.last_name, val.player1.first_name, " Score:", val.player1.tmp_score)
                print("Player:",val.player2.last_name, val.player2.first_name, " Score:", val.player2.tmp_score)


    def display_tournament_result(self, players):
        """ Display the players withe the total score of the tournament """
        print("\n=====   Tournament results   =====")
        for player in players:
            print("Player:",player.last_name, player.first_name, " Score:", player.score)


    def display_all_tournaments(self, tournaments):
        """ Display all tournaments details """
        print("\n==========   List of tournaments   ==========")
        if tournaments:
            print(tabulate(tournaments, headers=["name", "location", "date", "time type", "description"]))
        else:
            print("\tList is empty")        


    def display_all_players_sorted_by_alphabet(self, players):
        """ Display all players details from the tournaments by alphabet """
        print("\n==========   List of players by alphabet   ==========")
        if players:
            print(tabulate(players, headers=["last name", "first name", "birthdate", "gender", "score", "ranks"]))
        else:
            print("\t\tList is empty")  
            

    def display_all_players_sorted_by_ranks(self, players):
        print("\n==========   List of players by ranks   ==========")
        if players:
            print(tabulate(players, reverse = True), headers=["last name","first name", "ranks"])
        else:
            print("\t\tList is empty")             
