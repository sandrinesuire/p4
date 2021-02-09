"""Main file of chess application"""
from app.controlers import ApplicationController


class Application:
    """Class for Chess Application"""

    def __init__(self):
        """Method of initialize"""
        self.controller = ApplicationController()
        self.controller.start()


if __name__ == "__main__":
    Application()

