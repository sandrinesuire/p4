"""
Contain controller tournament
"""

from app import settings as s
from app.controllers.application import Controller, ApplicationController
from app.models.players import Player
from app.models.rounds import Round
from app.models.tournament import Tournament
from app.utils import Menu, MenuAction, Action

import sys

from typing import List, Tuple, Any, Union, Dict

from app.views.tournament import TournamentView


class TournamentController(Controller):
    """Class for Chess Tournament Controller"""

    tournament = None
    menu_touch = s.TOURNAMENT
    menu_text = f"| {s.TOURNAMENT} : Tournoi d'échecs"

    def __init__(self):
        """Initialize metod"""
        self.view = TournamentView()
        self.menu = Menu()
        self.menu.menu_actions.append(MenuAction(ApplicationController))
        self.menu.actions.append(Action(s.RANKING, "display_rank_menu", "ranking"))
        super(TournamentController, self).__init__()

    def start(self):
        """Method starting"""
        self.tournament = self.create_tournament()
        self.playing_tournament()
        sys.exit(self.view.get_quit_msg())

    def create_tournament(self) -> Tournament:
        """Method creating tournament from user information"""
        kwargs = self.get_infos_from_messages(self.view.creation_tournament_input_msg())
        tournament = Tournament(**kwargs)
        return tournament

    def playing_tournament(self):
        """Method playing the tournament"""
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

        ordered_players = sorted(self.tournament.players, key=lambda x: (-x.point,
                                                                         x.ranking))
        self.view.display_end_tournament_ranking_msg(ordered_players)
        for player in ordered_players:
            ranking = self.input(self.view.get_ranking_player_input_msg(player), False)
            player.ranking = ranking

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
        kwargs = self.get_infos_from_messages(
            self.view.get_first_last_name_player_input_msg())
        player = Player.get(kwargs)
        if not player:
            player = self.create_player(kwargs)
        return player

    def create_player(self, kwargs) -> Player:
        """Method creating player from user information"""
        kwargs_add = self.get_infos_from_messages(self.view.creation_player_input_msg())
        kwargs.update(kwargs_add)
        player = Player(**kwargs)
        return player

    def add_rounds(self) -> List[Round]:
        """Method generating rounds of tournament"""
        for player in self.tournament.players:
            player.update(point=0)
        rounds = []
        for num in range(self.tournament.rounds_number):
            round = Round(round_num=(num+1))
            rounds.append(round)
        return rounds

    def generate_matches(self, round: Round):
        """Method generating players pairs rounds of tournament"""
        if round.round_num == 1:
            round.matches = self.generate_first_round_matches()
        else:
            round.matches = self.generate_other_rounds_matches()
        self.tournament.save()

    def generate_first_round_matches(self) -> List[Tuple[list, List[Union[list, Any]]]]:
        """Method generating players pairs for first round of tournament"""
        matches = []
        end = (self.tournament.players_number // 2) * 2
        ordered_players = sorted(self.tournament.players[0:end],
                                 key=lambda x: (x.point, -x.ranking))
        middle = self.tournament.players_number // 2
        for num in range(middle):
            sup_player = ordered_players[num]
            inf_player = ordered_players[num + middle]
            matches.append(([sup_player, sup_player.point], [inf_player,
                                                             inf_player.point]))
        return matches

    def generate_other_rounds_matches(self) -> List[Tuple[list,
                                                          List[Union[list, Any]]]]:
        """Method generating players pairs for other rounds of tournament"""
        matches = []
        end = (self.tournament.players_number // 2) * 2
        ordered_players = sorted(self.tournament.players[0:end],
                                 key=lambda x: (-x.point, x.ranking))
        for num in range(0, end, 2):
            player1 = ordered_players[num]
            player2 = ordered_players[num+1]
            matches.append(([player1, player1.point], [player2, player2.point]))
        return matches

    def register_results_for_round(self, round: Round):
        """Method registrering matches results"""
        for match in round.matches:
            player1 = match[0][0]
            player2 = match[1][0]
            result = self.input(self.view.register_result_for_round_input_msg(
                player1, player2))
            if result == 0:
                player1.point += 0.5
                player2.point += 0.5
            elif result == 1:
                player1.point += 1
            elif result == 2:
                player2.point += 1

    def ranking(self):
        """Method modifing the rank of player """
        if self.tournament and self.tournament.players:
            ordered_players = sorted(self.tournament.players,
                                     key=lambda x: (-x.point, x.ranking))
            self.view.display_players_ranking(ordered_players)

            num = self.input(self.view.get_choosing_players_input_msg(), False)
            player = [player for player in self.tournament.players if
                      player.indice == num][0]
            ranking = self.input(self.view.get_ranking_player_input_msg(player), False)

            player.ranking = ranking
        else:
            self.view.display_no_players()

    def get_infos_from_messages(self, messages: Any) -> Dict[Any]:
        """Method collecting infos for tournament creation"""
        kwargs = {}
        for k, message in messages.items():
            answer = self.input(message, False)
            kwargs[k] = answer
        return kwargs
