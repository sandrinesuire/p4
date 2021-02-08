"""Main file of chess application"""
from app.controlers import ApplicationController

"""
- les print et messages sont dans les vues
- les input et la mise à jour de tes modèles sont dans les contrôleurs
- la logique métier est centrée dans les modèles (récupération des scores, d'un tour de
tournoi, update, création, etc.). Ce sont aussi les modèles qui dialoguent directement 
avec la base de données.
"""


class Application:
    """Class for Chess Application"""

    def __init__(self):
        """Method of initialize"""
        self.controller = ApplicationController()
        self.controller.start()


if __name__ == "__main__":
    Application()

