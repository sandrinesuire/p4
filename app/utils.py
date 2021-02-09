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
        self.menu_text = controller.view.menu_text


class Menu:

    menu_actions = []
    actions = []
    def __init__(self):
        self.menu_actions = []
        self.actions = []