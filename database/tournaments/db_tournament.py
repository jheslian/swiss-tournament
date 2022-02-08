from tinydb import TinyDB, Query, where
from tinydb.operations import add
from models.tournament import Tournament
import database.players.db_players as db_player

q = Query()
db = TinyDB('database/tournaments/tournament.json')
tournaments_table = db.table('tournaments')


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
        "finished": tournament.finished
    }
    tournaments_table.insert(serialize_tournament)


def start_playing(t_id):
    """ Modify state of tournament and update playing state """
    return tournaments_table.update({'playing': True}, doc_ids=[t_id])


def ended(t_id):
    """ Modify state of tournament and update playing state """
    return tournaments_table.update({'playing': False, 'finished': True}, doc_ids=[t_id])


def get_tournaments():
    """ Retrieve all tournaments """
    return tournaments_table.all()


def get_tournaments_to_play():
    """ Available tournaments to play """
    res = tournaments_table.search(where('finished') == False)
    if not res:
        return None
    return res


def add_players_id(t_id, tournament):
    """ Add players id to the tournaments database"""
    return tournaments_table.update({"players_id": tournament.players_ids}, doc_ids=[t_id])


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


def update_rounds(t_id, t_round):
    """ Add rounds to tournament """
    round = []
    content = {"name": t_round.name, "matches": [], "start_datetime": t_round.start_datetime,
               "end_datetime": t_round.end_datetime}
    matches = []
    match = {}

    for n, pair in enumerate(t_round.list_of_match[0]):
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
    round.append(content)
    return tournaments_table.update(add('rounds', [{str(t_round.name): round}]), doc_ids=[t_id])


def deserialize(t_id):
    val = tournaments_table.get(doc_id=int(t_id))
    players = db_player.deserialize(val['players_id'])

    tournament = Tournament()
    tournament.name = val["name"]
    tournament.location = val["location"]
    tournament.tournament_date = val["tournament_date"]
    tournament.description = val["description"]
    tournament.no_of_rounds = val["no_of_rounds"]
    tournament.no_of_players = val["no_of_players"]
    tournament.players = players
    tournament.rounds = val["rounds"]
    tournament.playing = True
    return tournament
