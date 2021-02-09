class Action:

    def __init__(self, menu_touch, menu_text, action):

        self.menu_touch = menu_touch
        self.menu_text = menu_text
        self.action = action


class MenuAction:

    controller = None

    def __init__(self, controller):
        self.controller = controller
        self.menu_touch = controller.menu_touch
        self.menu_text = controller.menu_text


class Menu:

    menu_actions = []
    actions = []
    def __init__(self):
        self.menu_actions = []
        self.actions = []


class CustomInput:

    menu = None
    view = None

    def __init__(self, handler):
        self.handler = handler
        self.print_menu()

    def __call__(self, message="", print_menu=True):
        if isinstance(message, str):
            message = (message, str)
        if print_menu:
            self.print_menu()

        answer_t = message[0]
        menu_action_answers = [m_action.menu_touch for m_action in self.handler.menu.menu_actions]
        action_answers = [action.menu_touch for action in self.handler.menu.actions]

        answer = None
        while not answer:
            answer = message[1](input(answer_t))
            if answer in menu_action_answers:
                controller = [m_action.controller for m_action in self.handler.menu.menu_actions if answer == m_action.menu_touch][0]
                return controller().start()
            elif answer in action_answers:
                action = [action.action for action in self.handler.menu.actions if answer == action.menu_touch][0]
                answer = getattr(self.handler, action)()
            if len(message) == 3 and answer not in message[2]:
                answer = None
            else:
                return answer

    def print_menu(self):
        print("| _______________________")
        if self.handler.menu.menu_actions:
            for m_action in self.handler.menu.menu_actions:
                print(m_action.menu_text)
        if self.handler.menu.actions:
            for action in self.handler.menu.actions:
                getattr(self.handler.view, action.menu_text)()
        print("| _______________________\n")