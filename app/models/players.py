"""
Contain model player
"""

from datetime import datetime

from dateutil import parser
from tinydb import TinyDB, Query

from app.models.models import Manager


class Player(Manager):
    """Class of Player Chess"""

    db = TinyDB('chess.json')
    table_name = 'players'
    table = db.table(table_name)

    def __init__(self, first_name: str, last_name: str, birth_date: str or datetime,
                 gender: str, ranking: int = None, point: int = None):
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
        self.save()

    def __str__(self):
        """Method returning data when str method is called"""
        return f"Joueur {self.first_name} {self.last_name}"

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
