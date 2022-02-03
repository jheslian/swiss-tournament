from tinydb import TinyDB, Query, where

Tournament = Query()
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
        "rounds": tournament.rounds,
        "players_id": tournament.players_ids,
        "playing": tournament.playing,
    }
    tournaments_table.insert(serialize_tournament)


def start_playing(tournament):
    print(tournament)
    """ Modify state of tournament and update playing state """
    return tournaments_table.update({'playing': True}, where('name') == str(tournament.name))


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
    return tournaments_table.update({"players": tournament.players_ids}, where('name') == str(tournament.name))


def update_rounds(tournament):
    """ Add rounds to tournament """
    rounds = []

    for val in tournament.rounds:
        print('r', val)
        content = {
            "name": val.name,
            "match": [],
            "start_datetime":  val.start_datetime,
            "end_datetime":  val.end_datetime
        }

        print("pair",val.name, val.start_datetime, val.end_datetime)
        print("mat", val.list_of_match)
        for con in val.list_of_match:
            for p in con:
                print("sq",p, type(p))

                print(p.player1.last_nam, p.player1.first_name, p.player1.score)


                """print("ssss",p, p[0], type(p), type(p[0]) )
                print(p.player[0].last_name, p.player1.first_name, p.player1.score)
                match = {
                    "last_name": p.player1.last_name,
                    "first_name": p.player1.first_name,
                    "score": p.player1.score
                }
                content["match"].append(match)
    return tournaments_table.update({"rounds": content}, where('name') == str(tournament.name))
"""
def get_rounds():
    """ Retrieve rounds of a tournament """
    pass


def get_matches():
    """ Retrieve matches of a tournament """
    pass