import sys

class View:
    # MENU
    def prompt_for_main_menu(self):
        """ prompt for main menu. """
        print("""
            ======   Main menu   ======
            ---------------------------
             t = Tournament
             m = Modify rank of a player
             q = Quit
            """
            )
        answer = input("choice: ")
        if answer == "t" or answer == "m":
            return answer
        elif answer == "q": 
            return self.quit()
        else: 
            print("option not found")
            return self.prompt_for_main_menu()

        
    def modify_player_rank(self, name):
        """ Modify player rank. """
        pass

    def prompt_for_tournament_menu(self):
        """ Tournament menu. """

        print("""
            ======   Tournament menu   ======
            ---------------------------------
            p = Play a tournament
            lt = List of tournaments
            3 = List of all players
            4 = Main menu
            """
            ) 
        answer = input("choice: ")
        if answer == "p" or answer == "lt":
            return answer
        elif answer == "3": 
            return self.quit()
        else: 
            print("option not found")
            return self.prompt_for_tournament_menu()  


    def display_list_of_tournaments(self, tournaments):
        print(
            "======   List of tournaments   ======\
             -------------------------------------"
            )
        for tournament in tournaments:
            print(tournament)
        
        answer = input("Enter the name tournament to consult, or enter any keys to return to Tournament menu")
        if answer in tournaments:
            return self.prompt_for_specific_tournament(answer)
            
        else:
            return self.prompt_for_tournament_menu() 
    

    def quit(self):
        print("See you, bye!")
        sys.exit(0)     



    def prompt_for_specific_tournament(self, choice):
        print("""
            ======   {choice} tournament   ======\
             ---------------------------------\
             
            """
            ) 
        pass    

    def prompt_for_player_menu(self):
        print(
            "======   Player menu   ======\
             ---------------------------\
             1 = List of all players\
             2 = List of players per round\
            "
            )


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