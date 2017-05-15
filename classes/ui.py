"""Lists the structure of UI class."""
from colorama import Fore, Style


class UI:
    """Defines the UI class object."""

    def print_error(self, text):
        """Print error to console."""
        print(f"{Fore.RED}{text}{Style.RESET_ALL}")

    def print_selection(self, text):
        """Print selection to console."""
        print(f"\nYou selected {text}\n")

    def print_damage_dealt(self, source, target, damage, type):
        """Print damage done."""
        print(f"{source} deals {damage} {type} damage to {target}")

    def print_healing_done(self, source, target, damage, type):
        """Print healing done."""
        print(f"{source}'s {type} heals {target} for {damage}")

    def print_message(self, text):
        """Print generic text."""
        print(f"\n{text}")

    def print_victory(self, text):
        """Print victory text."""
        print(f"\n{Fore.GREEN}{text}{Style.RESET_ALL}")

    def print_defeat(self, text):
        """Print defeat text."""
        print(f"\n{Fore.RED}{text}{Style.RESET_ALL}")

    def list_actions(self, actions):
        """Print a list of actions."""
        i = 1
        print()
        for action in actions:
            print(f"{i}: {action}")
            i += 1

    def list_spells(self, spells):
        """Print a list of spells."""
        i = 1
        for spell in spells:
            print(f"{i}: {spell.color}{spell.name}{Style.RESET_ALL} "
                  f"(cost: {spell.cost})")
            i += 1
        print(f"{i}: Cancel")

    def list_inventory(self, inventory):
        """Print the inventory list."""
        i = 1
        for item in inventory:
            name = item['item'].name
            desc = item['item'].description
            quantity = item['quantity']
            print(f"{i}: {name} ({desc}) x {quantity}")
            i += 1
        print(str(i) + ": Cancel")

    def print_columns(self, columnData, width=30):
        """Print list in a column format with a specified width."""
        for elements in columnData:
            print(f"{elements:<{width}}", end=" ")
        print()

    def print_hpmp(self, party, isPlayer=False):
        """Print hp and mp for all persons in a party list."""
        pNames = []
        pHp = []
        pMp = []
        for person in party:
            pHp.append(f"{Fore.GREEN}{person.hp}/"
                       f"{person.maxhp}{Style.RESET_ALL}")
            pMp.append(f"{Fore.CYAN}{person.mp}/"
                       f"{person.maxmp}{Style.RESET_ALL}")
            if isPlayer:
                pNames.append(f"{Fore.GREEN}{person.name}{Style.RESET_ALL}")
            else:
                pNames.append(f"{Fore.RED}{person.name}{Style.RESET_ALL}")
        self.print_columns(pNames)
        self.print_columns(pHp)
        self.print_columns(pMp)
        print()
