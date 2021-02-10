import sys

from app import settings as s
from app.controllers.tournament import TournamentController
from app.utils import CustomInput, Menu, MenuAction
from app.views.application import ApplicationView, QuitView


class Controller:
    """
    Class for generic controller
    """

    def __init__(self):
        """Initialize method"""
        self.input = CustomInput(self)


class ApplicationController(Controller):
    """
    Class for application
    """

    menu_touch = s.MAIN
    menu_text = f"| {s.MAIN} : Menu principal"

    def __init__(self):
        """Initialize metod"""
        self.view = ApplicationView()
        self.menu = Menu()
        self.menu.menu_actions.append(MenuAction(TournamentController))
        self.menu.menu_actions.append(MenuAction(QuitController))

        super(ApplicationController, self).__init__()

    def start(self):
        """Starting metod"""
        self.input("", False)


class QuitController(Controller):
    """Class for Application quit"""

    menu_touch = s.QUIT
    menu_text = f"| {s.QUIT} : Quitter"

    def __init__(self):
        """Initialize metod"""
        self.view = QuitView()
        super(QuitController, self).__init__()

    def start(self):
        """Starting metod"""
        sys.exit(self.view.get_quit_msg())