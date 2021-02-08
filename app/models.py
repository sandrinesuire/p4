"""File for chess models"""
import operator
from datetime import datetime
from enum import Enum
from functools import reduce

from dateutil import parser
from tinydb import TinyDB, Query, where

from app.settings import ROUNDS_NUMBER, PLAYERS_NUMBER


class Action:

    def __init__(self, answer_choice, answer_text, action):

        self.answer_choice = answer_choice
        self.answer_text = answer_text
        self.action = action


class MenuAction:
    controller = None

    def __init__(self, controller, answer_choice, answer_text):
        self.controller = controller
        self.answer_choice = answer_choice
        self.answer_text = answer_text

class Menu:

    menu_actions = []
    actions = []
    def __init__(self):
        self.menu_actions = []
        self.actions = []


class DBObject:
    
    indice = None
    db = TinyDB('chess.json')
    table_name = "default"
    table = db.table(table_name)

    def save(self):
        pass

    @classmethod
    def get(cls, kwargs):
        my_filter = []
        for k,v in kwargs.items():
            my_filter.append((where(k) == v))

        data = cls.table.search(reduce(operator.and_, my_filter))
        data = data[0] if data else None
        return cls.deserialize(data)

    @classmethod
    def deserialize(cls, data):
        if data:
            instance = cls(**data)
            instance.indice = data.doc_id
            return instance
        return

    @classmethod
    def get_n_first_instances(cls, instances_number):
        instances = []
        instances_list = cls.table.all()
        if instances_list:
            for i, player_data in enumerate(instances_list[0:instances_number]):
                instance = cls.deserialize(player_data)
                instances.append(instance)
            return instances

    @classmethod
    def existing_n_instances(cls, instances_number):
        instances_list = cls.table.all()
        return len(instances_list) >= instances_number

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()


class Player(DBObject):
    """Class of Player Chess"""

    db = TinyDB('chess.json')
    table_name = 'players'
    table = db.table(table_name)

    def __init__(self, first_name: str, last_name: str, birth_date, gender: str,
                 ranking: int = None, point: int = None):
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
        return f"Joueur {self.first_name} {self.last_name}"

    def save(self):
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


class TimeType(Enum):
    """Enum class of tournament time type"""

    BULLET = 'bullet'
    BLITZ = 'blitz'
    RAPID = 'rapid'


class Tournament(DBObject):
    """Class of Chess tournament"""

    db = TinyDB('chess.json')
    table_name = "tournaments"
    table = db.table(table_name)

    players = None
    rounds = []
    time_type: TimeType = None

    def __init__(self, name: str, location: str, tournament_date: datetime,
                 description: str, time_type: TimeType, rounds=None,
                 rounds_number=None, players_number=None):
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


class Round:
    """Class for round of chess tournament.

    The rules is swiss legality
    """
    round_num = None
    matches = None
    start_date = None
    end_date = None

    def __init__(self, round_num, start_date=None, end_date=None, matches=None):
        """Method initialize"""
        self.name = f"Round {round_num}"
        self.round_num = round_num
        if isinstance(start_date, str) and start_date != "None":
            start_date = parser.parse(start_date)
            self.start_date = start_date.date()
        if isinstance(end_date, str) and start_date != "None":
            end_date = parser.parse(end_date)
            self.end_date = end_date.date()
        if matches:
            self.matches = matches

    def __str__(self):
        return f"{self.name}"

    def start(self):
        self.start_date = datetime.now()

    def end(self):
        self.end_date = datetime.now()


