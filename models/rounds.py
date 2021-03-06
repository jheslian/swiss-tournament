""" Define rounds. """

from datetime import datetime


class Rounds:
    """Class for round of chess tournament."""

    def __init__(self, round_no: str = None, ):
        """ Initialize method """
        self.name = f"Round {round_no}"
        self.list_of_match = []
        self.start_datetime = None
        self.end_datetime = None

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def start(self):
        """ date and time when round is created """
        self.start_datetime = datetime.now().strftime('%d-%m-%Y, %H:%M:%S')
        return self.start_datetime

    def terminate(self):
        """ date and time when round is terminated """
        self.end_datetime = datetime.now().strftime('%d-%m-%Y, %H:%M:%S')
        return self.end_datetime
