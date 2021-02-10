from typing import Tuple, Any

from dateutil.parser import ParserError


class Action:
    """Class for MenuAction, allowing choose action in a application"""

    def __init__(self, menu_touch, menu_text, action):
        """Initialize metod"""
        self.menu_touch = menu_touch
        self.menu_text = menu_text
        self.action = action


class MenuAction:
    """Class for MenuAction, allowing choose menu action in a application"""

    def __init__(self, controller):
        """Initialize metod"""
        self.controller = controller
        self.menu_touch = controller.menu_touch
        self.menu_text = controller.menu_text


class Menu:
    """Class for Menu, allowing menu creation"""

    def __init__(self):
        """Initialize method"""
        self.menu_actions = []
        self.actions = []


class CustomInput:
    """Class representing input generic method overload with custom fonctionality"""
    menu = None
    view = None

    def __init__(self, controller):
        """Initialize metho"""
        self.controller = controller
        self.print_menu()

    def __call__(self, message: str or Tuple[Any] = "", print_menu: bool = True) -> Any:
        """Calling method. In more than input fonction calling, method checking if
        necessary to print menu or juste given text. With given text, a parse method is
        given, and some possible accepted answer (if no given, every answer is ok)"""
        if isinstance(message, str):
            message = (message, str)
        if print_menu:
            self.print_menu()

        answer_t = message[0]
        menu_action_answers = [m_action.menu_touch for m_action in self.controller.menu.menu_actions]
        action_answers = [action.menu_touch for action in self.controller.menu.actions]

        answer = None
        while not answer:
            try:
                answer = input(answer_t)
                answer = message[1](answer)
            except (ParserError, ValueError,):
                answer = None
            if answer in menu_action_answers:
                controller = [m_action.controller for m_action in self.controller.menu.menu_actions if answer == m_action.menu_touch][0]
                return controller().start()
            elif answer in action_answers:
                action = [action.action for action in self.controller.menu.actions if answer == action.menu_touch][0]
                answer = getattr(self.controller, action)()
            elif len(message) == 3 and answer not in message[2]:
                answer = None
            elif not message:
                return
        return answer

    def print_menu(self):
        """Method printing controller menu"""
        print("| _______________________")
        if self.controller.menu.menu_actions:
            for m_action in self.controller.menu.menu_actions:
                print(m_action.menu_text)
        if self.controller.menu.actions:
            for action in self.controller.menu.actions:
                getattr(self.controller.view, action.menu_text)()
        print("| _______________________\n")