"""View chess application"""
from typing import Dict, Tuple, Any, Type, List

from dateutil.parser import parse

from . import settings as s
from .models import Player


class ApplicationView:
    """View class for chess application"""

    def __init__(self):
        """Method of initialize"""
        print("\n| Menu Principal")


class QuitView:
    """View class for chess application"""

    def get_quit_msg(self) -> str:
        return f"Bye Bye"


class TournamentView:
    """View class for chess application"""

    def __init__(self):
        """Method of initialize"""
        print("\n| Menu Tournoie")

    """
    MENU TEXT
    """

    def get_quit_msg(self) -> str:
        return f"Bye Bye"

    def rank_menu(self):
        print(f"| {s.RANKING} : modifier le classement d'un joueur")

    """
    INPUT MESSAGE
    """

    def add_players_input_msg(self, complet=True) -> Tuple[str, Type[str], List[set]]:
        msg = f"\n{s.ADD_PLAYER} : ajouter un joueur\n"
        if complet:
            msg += f"{s.RANDOM_PLAYERS} : prendre aléatoiremenr les joueurs "
            return (msg, str, [s.ADD_PLAYER, s.RANDOM_PLAYERS])
        return (msg, str, [s.ADD_PLAYER,])

    def creation_tournament_input_msg(self) -> Dict[str, Tuple[str, Any]]:
        """Method returning message for ask creation tournament"""
        return {
            "name": ("Nom du tournoi : ", str),
            "location": ("Lieu du tournoi : ", str),
            "tournament_date": ("Date du tournoi (format 29-01-2021) : ", parse),
            "description": ("Description du tournoi : ", str),
            "time_type": ("Type de temps du tournoi (bullet, blitz, ou rapid) : ", str, ["bullet", "blitz", "rapid"]),
        }

    def creation_player_input_msg(self) -> Dict[str, Tuple[str, Any]]:
        """Method returning message for ask creation tournament"""
        return {
            "birth_date": ("Joueur non enregistré\nDate de naissance du joueur (format 29-01-2021) : ", parse),
            "gender": ("Genre du joueur (m masculin, f feminin) : ", str, [s.MALE, s.FEMININE]),
        }

    def get_first_last_name_player_input_msg(self) -> Dict[str, Tuple[str, Any]]:
        """Method returning message for ask creation tournament"""
        return {
            "first_name": ("Nom du nouveau joueur : ", str),
            "last_name": ("Prénom du joueur : ", str),
        }

    def register_result_for_round_input_msg(self, player1: Player, player2: Player) -> Tuple[
        str, Any, List[str]]:
        return (f"\nmatch: {str(player1)}/{str(player2)}\n{s.WIN_P1} : joueur 1 à"
                f" gagnant\n{s.WIN_P2} : joueur 2 gagnant"
                f" \n{s.WIN_NULL} : match null\nrésultat : ", int,
                [s.WIN_P1, s.WIN_P2, s.WIN_NULL])

    def get_start_input_msg(self, round) -> Tuple[str, Type[str], str]:
        response = "Liste des matchs : \n"
        for match in round.matches:
            response += f"{str(match[0][0])} contre {str(match[1][0])}\n"
        response += f"{round}\n{s.START_ROUND} : démarre le round"
        return (response, str, "d")

    def get_end_input_msg(self, round) -> Tuple[str, Type[str], str]:
        return (f"{round}\n{s.END_ROUND} : termine le round", str, "t")

    def get_ranking_players_input_msg(self) -> Tuple[str, Any, range]:
        rank_ok = range(1, s.PLAYERS_NUMBER + 1)
        return (f"Numero du joueur à modifier : ", int, rank_ok)

    def get_ranking_player_input_msg(self, player) -> Tuple[str, Any, range]:
        rank_ok = range(1, s.PLAYERS_NUMBER+1)
        return (f"{player.first_name} {player.last_name}\nClassement souhaité : ", int, rank_ok)

    """
    DISPLAY PRINT
    """

    def display_end_tournament_ranking_msg(self, players) -> str:
        response = ""
        for player in players:
            response += f"{player.first_name} {player.last_name} {player.point} points\n"
        response += "Merci de saisir le classement des joueurs\n"
        print(response)

    def display_players_ranking(self, players) -> str:
        response = "\n"
        for player in players:
            response += f"joueur N°{player.indice} {player.first_name} {player.last_name} Classement : {player.ranking}\n"
        print(response)

    def display_player(self, player):
        print(f"joueur {player.first_name} {player.last_name} créer\n")

    def display_no_players(self):
        print(f"\nMerci de composer l'équipe des joueurs avant de modifier leurs classement\n")



