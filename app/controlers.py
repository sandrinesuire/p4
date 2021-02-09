"""Controller file for chess application"""
import sys

from typing import List

from .models import Player, Tournament, Round
from .utils import Action, MenuAction, Menu, CustomInput
from . import settings as s
from .views import QuitView, TournamentView, ApplicationView


class Controller:
    """
    Class for generic controller
    """

    def __init__(self):
        """Initialize method"""
        self.input = CustomInput(self)
        self.menu = Menu()


class ApplicationController(Controller):
    """
    Class for application
    """

    view = ApplicationView
    menu_touch = s.MAIN
    menu_text = f"| {s.MAIN} : Menu principal"

    def __init__(self):
        self.view = ApplicationView()
        self.menu = Menu()
        self.menu.menu_actions.append(MenuAction(TournamentController))
        self.menu.menu_actions.append(MenuAction(QuitController))
        self.input = CustomInput(self)

    def start(self):
        self.input("", False)


class QuitController(Controller):
    view = QuitView
    menu_touch = s.QUIT
    menu_text = f"| {s.QUIT} : Quitter"

    def __init__(self):
        self.view = QuitView()
        self.input = CustomInput(self)

    def start(self):
        sys.exit(self.view.get_quit_msg())


class TournamentController(Controller):
    """Class for Chess Tournament Controller"""

    tournament = None
    menu_touch = s.TOURNAMENT
    menu_text = f"| {s.TOURNAMENT} : Tournoie d'échecs"

    def __init__(self):
        self.view = TournamentView()
        self.menu = Menu()
        self.menu.menu_actions.append(MenuAction(ApplicationController))
        self.menu.actions.append(Action(s.RANKING, "rank_menu", "ranking"))
        self.input = CustomInput(self)

    def ranking(self):
        if self.tournament and self.tournament.players:
            ordered_players = sorted(self.tournament.players,
                                     key=lambda x: (-x.point, x.ranking))
            self.view.display_players_ranking(ordered_players)

            num = self.input(self.view.get_ranking_players_input_msg(), False)
            player = [player for player in self.tournament.players if player.indice == num][0]
            ranking = self.input(self.view.get_ranking_player_input_msg(player), False)

            player.ranking = ranking
        else:
            self.view.display_no_players()

    def start(self):
        """Method starting tournament"""
        self.tournament = self.create_tournament()
        self.start_tournament()
        sys.exit(self.view.get_quit_msg())

    def start_tournament(self):
        self.tournament.players = self.add_players()
        self.tournament.rounds = self.add_rounds()
        self.tournament.save()
        for round in self.tournament.rounds:
            self.generate_matches(round)
            start = self.input(self.view.get_start_input_msg(round), True)
            if start:
                round.start()
            end = self.input(self.view.get_end_input_msg(round), False)
            if end:
                round.end()
            self.register_results_for_round(round)

        ordered_players = sorted(self.tournament.players, key=lambda x: (-x.point, x.ranking))
        self.view.display_end_tournament_ranking_msg(ordered_players)
        for player in ordered_players:
            ranking = self.input(self.view.get_ranking_player_input_msg(player), False)
            player.ranking = ranking

    def register_results_for_round(self, round):
        """Method registrering results"""
        for match in round.matches:
            player1 = match[0][0]
            player2 = match[1][0]
            result = self.input(self.view.register_result_for_round_input_msg(player1, player2))
            if result == 0:
                player1.point += 0.5
                player2.point += 0.5
            elif result == 1:
                player1.point += 1
            elif result == 2:
                player2.point += 1

    def add_rounds(self):
        """Method generating players pairs rounds of tournament"""
        for player in self.tournament.players:
            player.update(point=0)
        rounds = []
        for num in range(self.tournament.rounds_number):
            round = Round(round_num=(num+1))
            rounds.append(round)
        return rounds

    def generate_matches(self, round):
        """Method generating players pairs rounds of tournament"""
        if round.round_num == 1:
            round.matches = self.generate_first_round_matches()
        else:
            round.matches = self.generate_other_rounds_matches()
        self.tournament.save()

    def generate_first_round_matches(self):
        """Method generating players pairs for first round of tournament"""
        matches = []
        end = (self.tournament.players_number // 2) * 2
        ordered_players = sorted(self.tournament.players[0:end], key=lambda x: (x.point, -x.ranking))
        middle = self.tournament.players_number // 2
        for num in range(middle):
            sup_player = ordered_players[num]
            inf_player = ordered_players[num + middle]
            matches.append(([sup_player, sup_player.point], [inf_player, inf_player.point]))
        return matches

    def generate_other_rounds_matches(self):
        """Method generating players pairs for other rounds of tournament"""
        matches = []
        end = (self.tournament.players_number // 2) * 2
        ordered_players = sorted(self.tournament.players[0:end], key=lambda x: (-x.point, x.ranking))
        for num in range(0, end, 2):
            player1 = ordered_players[num]
            player2 = ordered_players[num+1]
            matches.append(([player1, player1.point], [player2, player2.point]))
        return matches

    def add_players(self) -> List[Player]:
        """Method adding players to tournament"""
        players = []
        complet = Player.existing_n_instances(s.PLAYERS_NUMBER)
        answer = self.input(self.view.add_players_input_msg(complet), True)
        if answer == s.RANDOM_PLAYERS:
            players = Player.get_n_first_instances(s.PLAYERS_NUMBER)
        else:
            missing_players_number = s.PLAYERS_NUMBER
            while missing_players_number:
                player = self.get_player()
                self.view.display_player(player)
                players.append(player)
                missing_players_number -= 1
        return players

    def get_player(self) -> Player:
        """Method getting player from user info"""
        kwargs = self.get_infos_from_messages(self.view.get_first_last_name_player_input_msg())
        player = Player.get(kwargs)
        if not player:
            player = self.create_player(kwargs)
        return player

    def create_tournament(self) -> Tournament:
        """Method creating tournament from user information"""
        kwargs = self.get_infos_from_messages(self.view.creation_tournament_input_msg())
        tournament = Tournament(**kwargs)
        return tournament

    def create_player(self, kwargs) -> Player:
        """Method creating tournament from user information"""
        kwargs_add = self.get_infos_from_messages(self.view.creation_player_input_msg())
        kwargs.update(kwargs_add)
        player = Player(**kwargs)
        return player

    def get_infos_from_messages(self, messages):
        """Method collecting infos for tournament creation"""
        kwargs = {}
        for k,message in messages.items():
            answer = self.input(message, False)
            kwargs[k] = answer
        return kwargs
