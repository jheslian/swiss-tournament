from tinydb import TinyDB, Query, where
from datetime import datetime
from tinydb.table import Document
from models.players import Player

q = Query()
db = TinyDB('database/players/player.json')
players_table = db.table('players')


def date_parser(date):
    return datetime.strftime(date, "%d-%m-%Y")


def save(player):
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
    """ Add players id to the tournaments database"""
    p = players_table.get(doc_id=player.id)
    score = p['score'] + float(player.tmp_score)
    played_with = p['played_with']
    played_with.extend(str(player.played_with[-1]))
    res = players_table.upsert(
        Document({"score": score, "tmp_score": float(player.tmp_score), "played_with": list(played_with)},
                 doc_id=player.id))
    if res is None:
        return None
    return res


def update_rank(p_id, p_new_rank):
    """ Update player rank """
    res = players_table.update({"rank": int(p_new_rank)}, doc_ids=[int(p_id)])
    if res is None:
        return None
    return res


def search_player(name):
    """ Search players """
    res = players_table.search(where('last_name') == name)
    if not res:
        return None
    return res


def get_players():
    """ Retrieve all tournaments """
    return players_table.all()


def get_match_players(players_id):
    """ Retrieve players from a tournament """
    players = []
    for p_id in players_id:
        players.append(players_table.get(doc_id=p_id))
    return players


def deserialize(players_id):
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
