"""
Contain model player
"""

from datetime import datetime
from typing import List

from dateutil import parser
from tinydb import TinyDB, Query

from app.models.models import Manager


class Player(Manager):
    """Class of Player Chess"""

    db = TinyDB('chess.json')
    table_name = 'players'
    table = db.table(table_name)

    def __init__(self, first_name: str, last_name: str, birth_date: str or datetime,
                 gender: str, opponent = None, ranking: int = None, point: int = None):
        """Method of initialize"""
        super(Player, self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        if isinstance(birth_date, str):
            birth_date = parser.parse(birth_date)
        self.birth_date = birth_date.date()
        self.gender = gender
        self.ranking = ranking or 0
        self.point = point or 0
        self.opponent = opponent or list() # if [] alors opponent à le même id pour tous les players ???
        self.save()

    def __hash__(self):
        """ Method for compare self with other. """
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        """Method returning data when str method is called"""
        return f"Joueur {self.first_name} {self.last_name}"

    def __key(self):
        """ Method returning key for special method """
        return (self.first_name, self.last_name)

    def save(self):
        """Saving method"""
        q = Query()
        indice = self.table.upsert({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": str(self.birth_date),
            "gender": self.gender,
            "ranking": self.ranking,
            "point": self.point,
        }, ((q.first_name == self.first_name) & (q.last_name == self.last_name)))
        self.indice = indice[0]
        return self

    def add_point(self, point: int):
        """ Method adding point. """
        self.point += point

    def add_opponent(self, player):
        """ Method adding opponent in opponent list. """
        self.opponent.append(player)

    def empty_opponent(self):
        """ Method emptying opponent list. """
        self.opponent = []

    def get_next_possible_player(self, players):
        """ Method testing if self could play with player. """
        for i, player in enumerate(players):
            if player not in self.opponent:
                return i
        raise ValueError("pb de joeurs ayant déjà joués ensemble")

