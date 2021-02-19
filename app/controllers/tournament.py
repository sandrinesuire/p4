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
        self.menu.add_menu_actions(MenuAction(ApplicationController))
        self.menu.add_actions(Action(s.RANKING, "display_rank_menu", "ranking"))
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
        self.tournament.add_players(self.add_players())
        self.tournament.add_rounds(self.add_rounds())
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
            player.update(ranking=ranking)

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
                if player not in players:
                    self.view.display_player(player)
                    players.append(player)
                    player.empty_opponent()
                    missing_players_number -= 1
                else:
                    self.view.player_chosed(player)
                    player = None
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
            round.add_matches(self.generate_first_round_matches())
        else:
            round.add_matches(self.generate_other_rounds_matches())
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
            sup_player.opponent.append(inf_player)
            inf_player.opponent.append(sup_player)
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
        for num in range(0, int(end/2)):
            player1 = ordered_players[0]
            ordered_players.remove(player1)
            i = player1.get_next_possible_player(ordered_players)
            player2 = ordered_players[i]
            ordered_players.remove(player2)
            player1.add_opponent(player2)
            player2.add_opponent(player1)
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
                player1.add_point(0.5)
                player2.add_point(0.5)
            elif result == 1:
                player1.add_point(1)
            elif result == 2:
                player2.add_point(1)

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

            player.update(ranking=ranking)
        else:
            self.view.display_no_players()

    def get_infos_from_messages(self, messages: Any) -> dict:
        """Method collecting infos for tournament creation"""
        kwargs = {}
        for k, message in messages.items():
            answer = self.input(message, False)
            kwargs[k] = answer
        return kwargs
