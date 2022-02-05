""" Define player. """


class Player:
    def __init__(self, last_name: str, first_name: str, birthdate: str, gender: str, rank=0, color: str = None):
        """ Player constructor """
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank
        self.score = 0
        self.tmp_score = 0
        self.played_with = []
        self.color = color
        self.id = None

    def __str__(self):
        return self.last_name

    def __repr__(self):
        """Used in print."""
        return self.last_name
