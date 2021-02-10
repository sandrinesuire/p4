from datetime import datetime
from enum import Enum
from typing import List

from dateutil import parser
from tinydb import TinyDB, Query

from app.models.models import Manager
from app.models.rounds import Round
from app.settings import ROUNDS_NUMBER, PLAYERS_NUMBER


class TimeType(Enum):
    """Enum class of tournament time type"""

    BULLET = 'bullet'
    BLITZ = 'blitz'
    RAPID = 'rapid'


class Tournament(Manager):
    """Class of Chess tournament"""

    db = TinyDB('chess.json')
    table_name = "tournaments"
    table = db.table(table_name)

    players = None
    rounds = []

    def __init__(self, name: str, location: str, tournament_date: datetime,
                 description: str, time_type: TimeType, rounds: List[Round] = None,
                 rounds_number: int = None, players_number: int = None):
        """Method of initialize"""
        super(Tournament, self).__init__()
        self.name = name
        self.location = location
        if time_type:
            self.time_type = time_type
        if isinstance(tournament_date, str):
            tournament_date = parser.parse(tournament_date)
        self.tournament_date = tournament_date.date()
        self. description = description
        if rounds_number:
            self.rounds_number = rounds_number
        else:
            self.rounds_number = ROUNDS_NUMBER
        if players_number:
            self.players_number = players_number
        else:
            self.players_number = PLAYERS_NUMBER
        if rounds:
            for round_data in rounds:
                round = Round(**round_data)
                self.rounds.append(round)
        self.save()

    def save(self):
        """Saving method"""
        q = Query()
        rounds = []
        for round in self.rounds:
            matches = []
            if round.matches:
                for match in round.matches:
                    matches.append(
                        {
                            "player1_first_name": match[0][0].first_name,
                            "player1_last_name": match[0][0].last_name,
                            "player2_first_name": match[1][0].first_name,
                            "player2_last_name": match[1][0].last_name,
                        }
                    )
                rounds.append(
                    {
                        "round_num": round.round_num,
                        "start_date": str(round.start_date),
                        "end_date": str(round.end_date),
                        "matches": matches,
                    }
                )
        indice = self.table.upsert({
            "name": self.name,
            "location": self.location,
            "tournament_date": str(self.tournament_date),
            "description": self.description,
            "time_type": self.time_type,
            "rounds_number": self.rounds_number,
            "players_number": self.players_number,
            "rounds": rounds
        }, ((q.tournament_date == str(self.tournament_date)) & (q.name == self.name)))
        self.indice = indice[0]
        return self
