from tinydb import TinyDB, Query, where

Player = Query()
db = TinyDB('database/players/player.json')
players_table = db.table('players')


def save(player):
    serialize_player = {
        "last_name": player.last_name,
        "first_name": player.first_name,
        "birth_date": player.birthdate,
        "gender": player.gender,
        "rank": player.rank,
        "score": player.score,
    }
    return players_table.insert(serialize_player)


def update_score(player):
    """ Add players id to the tournaments database"""
    res = players_table.update({"score": player.score}, doc_ids=[player.id])
    if res is None:
        return None
    return res


def update_rank(p_id, p_new_rank):
    """ Update player rank """
    res = players_table.update({"rank": p_new_rank}, doc_ids=[int(p_id)])
    if res is None:
        return None
    return res


def search_player(name):
    """ Search players """
    print("name", name)
    res = players_table.search(where('last_name') == name)
    if not res:
        return None
    return res


def get_players():
    """ Retrieve all tournaments """
    return players_table.all()

