"""Terminal Menu. A menu system for your terminal life.

This module provides users with tools to build simple, nestable, terminal based
menus. Each menu node is created independently and can be "linked" via the back
property to create "nested" menus.

TODO:
    * Identify a fix for massive traceback produced when navigating up and down
      a menu structure. Navigating into a sub menu and then selecting 'Back'
      causes two function calls to be added to the traceback. _Not sure if this
      is an actual issue._
"""
import os
import sys


class TerminalMenu:
    """TerminalMenu.

    TerminalMenu(prompt, options=None, back=False)

    Arguments:
        prompt (str): Menu prompt to be displayed above options.
        options (list): A list of option dictionaries.
                        An option dictionary consists of two mandatory keys,
                        ``text`` and ``func`` and one optional key ``args``.
                        ``text`` is the string displayed to the user under the
                        prompt. ``func`` is a callable that is executed when an
                        option is picked. ``args`` is a list passed to the
                        called ``func`` callable.
        back (function): If ``True`` then a 'Back' option will be appended to
                         this menu's options when they are printed. If this
                         option is selected the menu will return to the
                         previous menu where it will reprint its options.
    """

    def __init__(self, prompt, options=None, back=False):
        """Terminal Menu init."""
        self.__display = None
        self.__back = None
        self.__options = None
        self.__selected = None
        self.prompt = prompt
        self.back = back
        self.options = options

    def __display_options(self):
        """Print the menu into the terminal."""
        # os.system("cls")
        print(f"\n{self.prompt}\n{'-'*20}")
        backNumber = 1
        if self.options:
            backNumber = len(self.options) + 1
            for index, option in enumerate(self.options):
                print(f"{index + 1}. {option['text']}")
        if self.back:
            print(f"{backNumber}. Back")

    def __get_choice(self):
        """Return chosen option dictionary."""
        options = self.options
        while True:
            choice = input(">>> ")
            backNumber = 1
            if self.options:
                backNumber = len(self.options) + 1

            if not choice.isdigit():
                print("Please enter a number from the list")
                continue
            elif int(choice) == backNumber:
                return {"event": "back"}
            elif 0 <= (int(choice) - 1) <= (len(options) - 1):
                choice = int(choice) - 1
                return options[choice]
            else:
                print("Please enter a number from the list")

    def serve_menu(self, *args):
        """Display options, get user choice."""
        self.__display_options()
        self.selected = self.__get_choice()
        if "event" in self.selected:
            return self.selected
        elif len(args):
            return self.__choice_handler(args)
        else:
            return self.__choice_handler()

    def __choice_handler(self, args=None):
        """Handle choice function and optional args.

        If this is a sub-menu then the parent menu may have passed ``args`` to
        it. If this is the case then the ``args`` from the previous menu will
        be merged with the ``args`` associated with this menu's selected option
        and they will be passed to the option's ``func``.

        If the ``func`` key value returns a value and it is a dictionary with
        the key ``event`` and a value of ``back`` then this menu returns that
        dictionary to the parent menu where it triggers it to relist its
        options to the user.

        I'm really not happy with this logic.
        """
        func = self.selected["func"]
        funcReturn = None
        optionArgs = None

        if "args" in self.selected:
            optionArgs = self.selected["args"]

        if args and optionArgs:
            optionArgs += args
            funcReturn = func(optionArgs)
        elif args and not optionArgs:
            if len(args) == 1:
                funcReturn = func(args[0])
            else:
                funcReturn = func(args)
        elif not args and optionArgs:
            if len(optionArgs) == 1:
                funcReturn = func(optionArgs[0])
            else:
                funcReturn = func(optionArgs)
        else:
            funcReturn = func()

        if funcReturn:
            if "event" in funcReturn and funcReturn["event"] == "back":
                return self.serve_menu()
        return funcReturn

    def back_action(self):
        """Call function stored in ``self.back``."""
        return self.back()

    @property
    def options(self):
        """list: list of dictionary objects containing menu options."""
        return self.__options

    @options.setter
    def options(self, value):
        if type(value) == list or value is None:
            if value is None \
                    or not len(value) \
                    or all(type(x) is dict for x in value):
                self.__options = value
            else:
                raise TypeError(f"list index value must be dict,\
                                 not {type(value)}")
        else:
            raise TypeError(f"must be list or None, not {type(value)}")

    @property
    def back(self):
        """callable: function to call when ``self.back_action`` is called."""
        return self.__back

    @back.setter
    def back(self, value):
        if type(value) is bool:
            self.__back = value
        else:
            raise TypeError(f"must be bool, not {type(value)}")

    @property
    def display(self):
        """Return self.__display."""
        return self.__display

    @display.setter
    def display(self, value):
        if type(value) is str or value is None:
            self.__display = value
        else:
            raise TypeError(f"must be str or None, not {type(value)}")

    @property
    def selected(self):
        """Return self.__selected."""
        return self.__selected

    @selected.setter
    def selected(self, value):
        if type(value) is dict or value is None:
            self.__selected = value
        else:
            raise TypeError(f"must be dict or None, not {type(value)}")


if __name__ == "__main__":
    def join_print(args):
        """Join args and print the result."""
        joined = "".join(args)
        print(joined)

    def exit():
        """System exit."""
        os.system("cls")  # Windows Terminal "clear"
        sys.exit()

    mainMenu = TerminalMenu("Main Menu: Choose an option.")
    aFirstMenu = TerminalMenu("aFirst Menu: Choose an option.", back=True)
    bFirstMenu = TerminalMenu("bFirst Menu: Choose an option.", back=True)
    bSecondMenu = TerminalMenu("bSecond Menu: Choose an option.", back=True)
    emptyMenu = TerminalMenu("This is empty", back=True)

    mainMenu.options = [{"text": "aFirst Menu", "func": aFirstMenu.serve_menu},
                        {"text": "bFirst Menu", "func": bFirstMenu.serve_menu},
                        {"text": "Empty Menu", "func": emptyMenu.serve_menu},
                        {"text": "Exit", "func": exit}]

    aFirstMenu.options = [{"text": "Print 'foo'",
                           "func": print,
                           "args": ["foo"]}]

    bFirstMenu.options = [{"text": "Pass 'foo' to sub-menu",
                           "func": bSecondMenu.serve_menu,
                           "args": ["foo"]}]

    bSecondMenu.options = [{"text": "Join 'bar' with passed arg and print",
                            "func": join_print,
                            "args": ["bar"]}]

    mainMenu.serve_menu()
