"""Simple, nested, menu systems for terminals.

This module provides users with tools to build simple, nested, terminal based
menus.

Todo:
    * Finish module level comments
"""
import os
import sys


class TerminalMenu:
    """Terminal Menu class."""

    def __init__(self, options=None, back=None):
        """Init.

        Arguments:

        Properties:

        Todo:

        """
        self.__back = None
        self.__options = None
        self.back = back
        self.options = options

    def __display_options(self):
        """Print the menu into the terminal."""
        os.system('cls')
        print(f"\n{'='*20}")  # ====================
        for index, option in enumerate(self.options):
            print(f"{index+1}. {option['text']}")

    def __get_choice(self):
        """Return option function based on user choice."""
        while True:
            choice = input(">>> ")
            if not choice.isdigit():
                print("Please enter a number from the list")
                continue
            elif 0 <= int(choice) - 1 <= len(self.options):
                choice = int(choice) - 1
                return self.options[choice]["func"]
            else:
                print("Please enter a number from the list")

    def serve_menu(self):
        """Display options, get user choice and execute option function."""
        self.__display_options()
        return self.__get_choice()()

    def back_action(self):
        """Perform back action function."""
        self.back()

    @property
    def options(self):
        """Return options."""
        return self.__options

    @options.setter
    def options(self, value):
        """Set the value of self.__options."""
        if type(value) == list:
            self.__options = value

    @property
    def back(self):
        """Return self.__back."""
        return self.__back

    @back.setter
    def back(self, value):
        """Set the value of self.__back."""
        if callable(value):
            self.__back = value


if __name__ == "__main__":
    def bar():
        """Print bar."""
        return "bar"

    def baz():
        """Print baz."""
        return "baz"

    def exit():
        """System exit."""
        sys.exit()

    fooMenu = TerminalMenu()
    bazMenu = TerminalMenu(back=fooMenu.serve_menu)

    bazMenu.options = [{"text": "Print Baz", "func": baz},
                       {"text": "Cancel", "func": bazMenu.back_action}]

    fooMenu.options = [{"text": "Print Bar", "func": bar},
                       {"text": "Baz Menu", "func": bazMenu.serve_menu},
                       {"text": "Exit", "func": exit}]
    print(fooMenu.serve_menu())
