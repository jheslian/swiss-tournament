from tinydb import TinyDB, Query, where

Tournament = Query()
db = TinyDB('database/tournaments/tournament.json')
tournaments_table = db.table('tournaments')
# tournaments_table.truncate()


def save(tournament):
    """ Add tournament to database """
    serialize_tournament = {
        "name": tournament.name,
        "location": tournament.location,
        "tournament_date": tournament.tournament_date,
        "time_type": tournament.time_type,
        "description": tournament.description,
        "no_of_rounds": tournament.no_of_rounds,
        "no_of_players": tournament.no_of_players,
        "rounds": tournament.rounds,
        "players_id": tournament.players_ids,
        "playing": tournament.playing,
    }
    tournaments_table.insert(serialize_tournament)


def start_playing(condition, t_id):
    """ Modify state of tournament and update playing state """
    if condition is False:
        return tournaments_table.update({'playing': condition, 'players_id': []}, doc_ids=[t_id])
    return tournaments_table.update({'playing': condition}, doc_ids=[t_id])


def get_tournaments():
    """ Retrieve all tournaments """
    return tournaments_table.all()


def get_tournaments_to_play():
    """ Available tournaments to play """
    res = tournaments_table.search(where('playing') == False)

    if not res:
        return None
    return res


def add_players_id(tournament):
    """ Add players id to the tournaments database"""
    return tournaments_table.update({"players_id": tournament.players_ids}, where('name') == str(tournament.name))


def get_rounds(t_id):
    """ Retrieve rounds of a tournament """
    res = tournaments_table.get(doc_id=int(t_id))
    if not res['rounds']:
        return None
    return res['rounds']


def get_players(t_id):
    """ Return players of a tournament """
    res = tournaments_table.get(doc_id=int(t_id))
    if not res['players_id']:
        return None
    return res['players_id']


def update_rounds(tournament):
    """ Add rounds to tournament """
    rounds = []
    for val in tournament.rounds:
        content = {"name": val.name, "matches": [], "start_datetime": val.start_datetime,
                   "end_datetime": val.end_datetime}
        matches = []
        match = {}
        for n, pair in enumerate(val.list_of_match[0]):
            match["match" + str(n + 1)] = {
                "player1": {
                    "last_name": pair[0].last_name,
                    "first_name": pair[0].first_name,
                    "score": pair[0].tmp_score
                },
                "player2": {
                    "last_name": pair[1].last_name,
                    "first_name": pair[1].first_name,
                    "score": pair[1].tmp_score
                }
            }
            matches.append(match)
        content["matches"].append(match)
        rounds.append(content)
    return tournaments_table.update({"rounds": rounds}, where('name') == str(tournament.name))
