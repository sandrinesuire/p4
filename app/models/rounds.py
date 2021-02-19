"""
Contain model round
"""

from datetime import datetime
from typing import List

from dateutil import parser


class Round:
    """Class for round of chess tournament.

    The rules is swiss legality
    """

    def __init__(self, round_num, start_date=None, end_date=None, matches=None):
        """Method initialize"""
        self.name = f"Round {round_num}"
        self.round_num = round_num
        if isinstance(start_date, str) and start_date != "None":
            start_date = parser.parse(start_date)
            self.start_date = start_date.date()
        else:
            self.start_date = start_date
        if isinstance(end_date, str) and start_date != "None":
            end_date = parser.parse(end_date)
            self.end_date = end_date.date()
        else:
            self.end_date = end_date
        self.matches = matches

    def __str__(self):
        """Method returning data when str method is called"""
        return f"{self.name}"

    def start(self):
        """Method updating start date """
        self.start_date = datetime.now()

    def end(self):
        """Method updating end date """
        self.end_date = datetime.now()

    def add_matches(self, matches: List):
        """ Method adding matches to matches list. """
        self.matches = matches

