

# Swiss tournament
### A program that manage offline tournament events.
## Objectives:

- Create a MVC method with 4 Models(Tournament, Round, Match, and Player) and MVC codes are organised.
- Use tools such as flake8, Black or Isort as a code wrapper thats verifies code according to  PEP8.
- A program where swiss tournament regulations must be follow strictly and program that could:
	 - [ ] Create a tournament, players
	 - [ ] A match between players in each rounds
	 - [ ] Register the datas to a database using TinyDB
	 - [ ] A view or report of the ff:
			 1. List of all the players(sorted by alphabet and by ranks)
			 2. List of the players of a tournament(sorted by alphabet and by ranks)
			 3. List of all the tournaments
			 4. List of all the matches of a tournament
			 5. List of all the rounds of a tournament

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