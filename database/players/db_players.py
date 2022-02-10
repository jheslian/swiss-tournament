"""  Define player utils for database """
from tinydb import TinyDB, Query, where
from datetime import datetime
from tinydb.table import Document
from models.players import Player

q = Query()
db = TinyDB('database/players/player.json')
players_table = db.table('players')


def date_parser(date):
    """ parse str date input to type datetime

    Args:
        date (str): str to parse

    Returns:
        datetime: to store on player obj
    """
    return datetime.strftime(date, "%d-%m-%Y")


def save(player):
    """ Store players details to the database

    Args:
        player (player obj): convert object to dict

    Returns:
        int: players id
    """
    serialize_player = {
        "last_name": player.last_name,
        "first_name": player.first_name,
        "birth_date": date_parser(player.birthdate),
        "gender": player.gender,
        "rank": player.rank,
        "played_with": player.played_with,
        "score": player.score,
        "tmp_score": player.tmp_score,
    }
    return players_table.insert(serialize_player)


def update_score(player):
    """ Modify player score and store match score

    Args:
        player (player obj): player to modify
    """
    p = players_table.get(doc_id=player.id)
    score = p['score'] + float(player.tmp_score)
    played_with = p['played_with']
    played_with.extend(str(player.played_with[-1]))
    players_table.upsert(
        Document({"score": score, "tmp_score": float(player.tmp_score), "played_with": list(played_with)},
                 doc_id=player.id))


def update_rank(p_id, p_new_rank):
    """ Modify player rank

    Args:
        p_id (int): player id to modify
        p_new_rank (int): this replaces the previous rank
    """
    players_table.update({"rank": int(p_new_rank)}, doc_ids=[int(p_id)])


def search_player(name):
    """ Search a player

    Args:
        name (str): player name

    Returns:
        dict: all players that has the same name
    """
    res = players_table.search(where('last_name') == name)
    if not res:
        return None
    return res


def get_players():
    """ Retrieve all players

    Returns:
        dict: players found on the db
    """
    return players_table.all()


def get_match_players(players_id):
    """ Retrieve players of a tournament

    Args:
        players_id (list): players id to retrieve

    Returns:
        dict: players details
    """
    players = []
    for p_id in players_id:
        players.append(players_table.get(doc_id=p_id))
    return players


def deserialize(players_id):
    """Convert data from database to obj

    Args:
        players_id (list): players to retrieve

    Returns:
        players obj: players converted from from db
    """
    dict_players = get_match_players(players_id)
    players = []
    for p in dict_players:
        player = Player()
        player.last_name = p['last_name']
        player.first_name = p['first_name']
        player.birthdate = p['birth_date']
        player.gender = p['gender']
        player.rank = p['rank']
        player.played_with = p['played_with']
        player.score = p['score']
        player.id = p.doc_id
        players.append(player)
    return players
