"""Lists the structure of UI class."""
from colorama import Fore, Style


class UI:
    """Defines the UI class object."""

    def print_error(self, text):
        """Print error to console."""
        print(Fore.RED + text + Style.RESET_ALL)

    def print_selection(self, text):
        """Print selection to console."""
        print("\nYou selected", text, "\n")

    def print_damage_dealt(self, source, target, damage, type):
        """Print damage done."""
        print(f"{source} deals {damage} {type} damage to {target}")

    def print_healing_done(self, source, target, damage, type):
        """Print healing done."""
        print(f"{source}'s {type} heals {target} for {damage}")

    def print_message(self, text):
        """Print generic text."""
        print("\n", text)

    def list_actions(self, actions):
        """Print a list of actions."""
        i = 1
        print()
        for action in actions:
            print(str(i) + ":", action)
            i += 1

    def list_spells(self, spells):
        """Print a list of spells."""
        i = 1
        for spell in spells:
            print(str(i) + ":", spell.color + spell.name + Style.RESET_ALL,
                  "(cost:", str(spell.cost) + ")")
            i += 1
        print(str(i) + ": Cancel")

    def print_hpmp(self, player, enemy):
        """Print hp and mp for all persons."""
        print("\n===Your Turn===")
        print("Enemy HP:", Fore.MAGENTA + Style.DIM, enemy.get_hp(), "/",
              enemy.get_max_hp(), Style.RESET_ALL)
        print("Player HP:", Fore.GREEN, player.get_hp(), "/",
              player.get_max_hp(), Style.RESET_ALL, "\nPlayer MP:", Fore.CYAN,
              player.get_mp(), "/", player.get_max_mp(), Style.RESET_ALL)
