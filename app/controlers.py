"""Controller file for chess application"""
import sys

from typing import List

from .models import Player, Tournament, Round, Menu, MenuAction, Action
from .settings import PLAYERS_NUMBER, QUIT, RANKING, RANDOM_PLAYERS, TOURNAMENT, MAIN
from .views import QuitView, TournamentView, ApplicationView


class Controller:

    menu = None

    def input(self, text=""):
        answer_t = "_______________________\n"
        for m_action in self.menu.menu_actions:
            answer_t += m_action.answer_text
        for action in self.menu.actions:
            answer_t += action.answer_text
        answer_t += "_______________________\n"
        answer_t += text
        menu_action_answers = [m_action.answer_choice for m_action in
                               self.menu.menu_actions]
        action_answers = [action.answer_choice for action in self.menu.actions]
        answer = None
        while not answer:
            answer = input(answer_t)
            if answer in menu_action_answers:
                controller = \
                [m_action.controller for m_action in self.menu.menu_actions if
                 answer == m_action.answer_choice][0]
                return controller().start()
            elif answer in action_answers:
                action = [action.action for action in self.menu.actions if
                          answer == action.answer_choice][0]
                return getattr(self, action)()
            elif text:
                return answer
            else:
                answer = None

    def start(self):
        self.input()


class ApplicationController(Controller):

    def __init__(self):
        self.view = ApplicationView()
        self.menu = Menu()
        self.menu.menu_actions.append(MenuAction(TournamentController, TOURNAMENT, TournamentView.tournament_msg()))
        self.menu.menu_actions.append(MenuAction(QuitController, QUIT, QuitView.start_msg()))


class QuitController:

    def __init__(self):
        self.view = QuitView()
        sys.exit(self.view.quit_msg())


class TournamentController(Controller):
    """Class for Chess Tournament Controller"""

    tournament = None
    view = None

    def __init__(self):
        self.menu = Menu()
        self.view = TournamentView()
        self.menu.menu_actions.append(MenuAction(ApplicationController, MAIN, ApplicationView.start_msg()))
        self.menu.actions.append(Action(RANKING, self.view.rank_menu_msg(), "ranking"))

    def ranking(self):
        if self.tournament and self.tournament.players:
            ordered_players = sorted(self.tournament.players,
                                     key=lambda x: (-x.point, x.ranking))
            self.view.display_players_ranking(ordered_players)

            num = self.get_info_from_message(self.view.get_ranking_players_input_msg())
            player = [player for player in self.tournament.players if player.indice == num][0]
            ranking = self.get_info_from_message(self.view.get_ranking_player_input_msg(player))

            player.ranking = ranking
        else:
            self.view.display_no_players()

    def get_menu(self):
        menu = self.view.quit_menu_msg()
        if self.tournament and self.tournament.players:
            menu += self.view.rank_menu_msg()
        return menu

    def start(self):
        """Method starting tournament"""
        self.tournament = self.create_tournament()
        self.start_tournament()
        sys.exit(self.view.quit_msg())

    def start_tournament(self):
        self.tournament.players = self.add_players()
        self.tournament.rounds = self.add_rounds()
        self.tournament.save()
        for round in self.tournament.rounds:
            self.generate_matches(round)
            start = self.get_info_from_message(self.view.get_start_input_msg(round))
            if start:
                round.start()
            end = self.get_info_from_message(self.view.get_end_input_msg(round))
            if end:
                round.end()
            self.register_results_for_round(round)

        ordered_players = sorted(self.tournament.players, key=lambda x: (-x.point, x.ranking))
        self.view.display_end_tournament_ranking_msg(ordered_players)
        for player in ordered_players:
            ranking = self.get_info_from_message(self.view.get_ranking_player_input_msg(player))
            player.ranking = ranking
        sys.exit(self.view.quit_msg())

    def register_results_for_round(self, round):
        """Method registrering results"""
        for match in round.matches:
            player1 = match[0][0]
            player2 = match[1][0]
            message = self.view.register_result_for_round_input_msg(player1, player2)
            result = self.get_info_from_message(message)
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
        for num in range(0,end,2):
            player1 = ordered_players[num]
            player2 = ordered_players[num+1]
            matches.append(([player1, player1.point], [player2, player2.point]))
        return matches

    def add_players(self) -> List[Player]:
        """Method adding players to tournament"""
        players = []
        complet = Player.existing_n_instances(PLAYERS_NUMBER)
        answer = self.get_info_from_message(self.view.add_players_input_msg(complet))
        if answer == RANDOM_PLAYERS:
            players = Player.get_n_first_instances(PLAYERS_NUMBER)
        else:
            missing_players_number = PLAYERS_NUMBER
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
        messages = self.view.creation_tournament_input_msg()
        kwargs = self.get_infos_from_messages(messages)
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
        for k,v in messages.items():
            answer = None
            while not answer:
                answer_inp = self.input(v[0])
                try:
                    answer = v[1](answer_inp)
                    if len(v) == 3:
                        if answer not in v[2]:
                            answer = None
                    if answer:
                        kwargs[k] = answer
                except:
                    answer = None

        return kwargs

    def get_info_from_message(self, message):
        """Method collecting infos for tournament creation"""
        answer = None
        while not answer:
            answer_inp = self.input(message[0])
            try:
                answer = message[1](answer_inp)
                if len(message) == 3:
                    if answer not in message[2]:
                        answer = None
            except:
                answer = None

        return answer
