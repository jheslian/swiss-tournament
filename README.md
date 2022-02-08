

# Swiss tournament
### A program that manage offline tournament events.

## Objectives:

- Create a MVC method with 4 Models(Tournament, Round, Match, and Player) and MVC codes are organised.
- Use tools such as flake8, Black or Isort as a code wrapper thats verifies code according to  PEP8.
- A program where swiss tournament regulations must be follow strictly and program that could:
	 - [x] Create a tournament, players
	 - [x] A match between players in each rounds
	 - [x] Register the datas to a database using TinyDB
	 - [x] A view or report of the ff:
			 1. List of all the players(sorted by alphabet and by ranks)
			 2. List of the players of a tournament(sorted by alphabet and by ranks)
			 3. List of all the tournaments
			 4. List of all the matches of a tournament
			 5. List of all the rounds of a tournament
			 
***How pairing works:***
- The first round is sorted by ranks and paired accordingly with this example:
example of 8 players : A B C D E	F G H	-> pairing result =	 A vs E, B vs F, C vs G and D vs G while the rest of the rounds are paired with the same score as them or if the players score's are all equal then it will be sorted by ranks: pairing result from the 8 players = A vs B, C vs D, E vs F, and G vs H. 
- Players cannot play the same opponent more than once in the same tournament.

## Getting started:
**Note**: Make sure you have python, virtual environment and git on your machine : 
	- `python -V` : command to check the version python if its installed
	- verify that you have the venv module : `python -m venv --help` if not please check https://www.python.org/downloads/. You could also use any other virtual environment to run the program(**if you opted to use other virtual environment the next commands are not suitable to run the program**)
	- `git --version` : to check your git version if its installed or you could download it at https://git-scm.com/downloads
 1. Clone the repository on the terminal or command prompt : `git clone git@github.com:jheslian/swiss-tournament.git`
 2. Create a virtual environment with "venv"  
	 - `cd swiss-tournament` :  to access the folder 
	 - python -m venv ***environment name*** : to create the virtual environment - exemple: `python -m venv env`
3. Activate the virtual environment:
	for unix or macos:
	- source ***environment name***/bin/activate - ex : `source env/bin/activate` if "env" is used as environment name 
	for windows:
	- ***environment name***\Scripts\activate.bat - ex: `env\Scripts\activate.bat`
4. Install the packages with pip: `pip install -r requirements.txt`	
6. Run the program : 
	for unix or macos: `python3 main.py`
	for windows: `py main.py`

## How to play:
**Menu:** - Menu for the tournament
**c**      -     Create a tournament (a tournament created can be played in the future too)
**p**      -     Play a tournament (choose a tournament to begin)
**lt**     -     List of tournaments (View of all the tournaments registered)
**lr**     -     List of rounds of a tournament (details of rounds played in a selected tournament)
**lm**    -      List of matchs of a tournament (details of matches played in a selected tournament)
**lp**      -    List of players of a tournament (details of players in a selected tournament, sorted by rank and alphabetically)
**ap**    -      List of all players sorted alphabetically (players of all the tournaments completed or not)
**rp**      -    List of all players sorted by ranks
**ur**      -    Update player rank (modify the rank of a player)
**q**      -     Quit

 - Create tournament to start
 - Play the tournament by entering the tournament id
 - Enter the details of the players
 - Enter the last name of the winner of each match on each round until its over (winner will have 1pt and if player is entered the match is tie like stated ont the program)

***Note:  An option is provided before each round of match to play directly or continue the match in the future ***
