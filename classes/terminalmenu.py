"""Terminal Menu.

This module provides users with tools to build simple, nestable, terminal based
menus. Each menu node is created independently and can be "linked" via the back
property to create "nested" menus.



Todo:
    * Finish module level comments
    * Throw exceptions when invalid setter values supplied
    * Add unit tests (to ../tests/)
"""
import os
import sys


class TerminalMenu:
    """Terminal Menu Class."""

    def __init__(self, display, options=None, back=None):
        """Terminal Menu class init.

        Args:
            display (str): Text to display above menu options.
            options (list): A list of option dictionaries.
            back (function): A function to be called via ``back_action``
        """
        self.__display = None
        self.__back = None
        self.__options = None
        self.__selected = None
        self.display = display
        self.back = back
        self.options = options

    def __display_options(self):
        """Print the menu into the terminal."""
        # os.system("cls")
        print(f"\n{self.display}\n{'-'*20}")
        if self.options:
            for index, option in enumerate(self.options):
                print(f"{index + 1}. {option['text']}")
            if self.back:
                print(f"{len(self.options) + 1}. Back")
        else:
            if self.back:
                print(f"1. Back")

    def __get_choice(self):
        """Return option dictionary based on user choice."""
        options = self.options
        while True:
            choice = input(">>> ")
            if self.options:
                if not choice.isdigit():
                    print("Please enter a number from the list")
                    continue
                elif 0 <= (int(choice) - 1) <= (len(options) - 1):
                    choice = int(choice) - 1
                    return options[choice]
                elif int(choice) == len(options) + 1:
                    self.back_action()
                else:
                    print("Please enter a number from the list")
            else:
                if not choice.isdigit():
                    print("Please enter a number from the list")
                elif int(choice) == 1:
                    self.back_action()
                else:
                    print("Please enter a number from the list")

    def serve_menu(self, *args):
        """Display options, get user choice."""
        self.__display_options()
        self.selected = self.__get_choice()
        if len(args):
            return self.__choice_handler(args)
        else:
            return self.__choice_handler()

    def __choice_handler(self, args=None):
        """Handle choice function and optional args."""
        if self.selected["func"].__name__ == "back_action":
            return self.back_action()

        func = self.selected["func"]
        choiceArgs = None
        if "args" in self.selected:
            choiceArgs = self.selected["args"]

        if args and choiceArgs:
            choiceArgs += args
            return func(choiceArgs)
        elif args and not choiceArgs:
            if len(args) == 1:
                return func(args[0])
            else:
                return func(args)
        elif not args and choiceArgs:
            if len(choiceArgs) == 1:
                return func(choiceArgs[0])
            else:
                return func(choiceArgs)
        else:
            return func()

    def back_action(self):
        """Call function stored in ``self.back``."""
        self.back()

    @property
    def options(self):
        """list: list of dictionary objects containing menu options."""
        return self.__options

    @options.setter
    def options(self, value):
        if type(value) == list:
            self.__options = value

    @property
    def back(self):
        """callable: function to call when ``self.back_action`` is called."""
        return self.__back

    @back.setter
    def back(self, value):
        if callable(value):
            self.__back = value

    @property
    def display(self):
        """Return self.__display."""
        return self.__display

    @display.setter
    def display(self, value):
        """Set the value of self.__display."""
        if type(value) == str:
            self.__display = value

    @property
    def selected(self):
        """Return self.__selected."""
        return self.__selected

    @selected.setter
    def selected(self, value):
        """Set the value of self.__selected."""
        if type(value) == dict:
            self.__selected = value


if __name__ == "__main__":
    from random import randrange

    # os.system("cls")  # Clear terminal (windows variant)

    # Test functions
    def attack(args):
        """Return random attack value as formatted string."""
        target = args
        print(f"Attacked {target} for {randrange(50, 150)}!")

    def cast_spell(args):
        """Return random spell value as formatted string."""
        target, spell = args
        print(f"Attacked {target} with {spell} for {randrange(50, 150)}!")

    def exit():
        """System exit."""
        os.system("cls")
        sys.exit()

    # Define menu "shells"
    actionMenu = TerminalMenu("Choose an action")
    atkTargetMenu = TerminalMenu("Choose a target", back=actionMenu.serve_menu)
    spellMenu = TerminalMenu("Choose a spell", back=actionMenu.serve_menu)
    splTargetMenu = TerminalMenu("Choose a target", back=spellMenu.serve_menu)

    # Define menu options (bottom up)
    atkTargetMenu.options = [{"text": "Gerblin", "func": attack,
                              "args": ["gerblin"]},
                             {"text": "Bepis", "func": attack,
                              "args": ["bepis"]},
                             {"text": "Cancel",
                              "func": atkTargetMenu.back_action}]

    spellMenu.options = [{"text": "Fireball", "func": splTargetMenu.serve_menu,
                          "args": ["fireball"]},
                         {"text": "Blizzard", "func": splTargetMenu.serve_menu,
                          "args": ["blizzard"]},
                         {"text": "Cancel", "func": spellMenu.back_action}]

    splTargetMenu.options = [{"text": "Gerblin", "func": cast_spell,
                              "args": ["gerblin"]},
                             {"text": "Bepis", "func": cast_spell,
                              "args": ["bepis"]},
                             {"text": "Cancel",
                              "func": splTargetMenu.back_action}]

    actionMenu.options = [{"text": "Attack", "func": atkTargetMenu.serve_menu},
                          {"text": "Spell", "func": spellMenu.serve_menu},
                          {"text": "Exit", "func": exit}]

    # Serve up a hot and delicious option menu.
    actionMenu.serve_menu()
