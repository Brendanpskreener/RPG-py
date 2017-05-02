"""Lists the structure of the game class."""
from colorama import Fore, Style
from classes.person import Person
from classes.spell import Spell
from classes.item import Item
from classes.ui import UI


class Game:
    """Defines the Game class object."""

    def __init__(self):
        """Docstring for Game initialization."""
        # Create spell
        playerSpells = [
            Spell("Fire", 10, 60, "black", Fore.RED + Style.BRIGHT),
            Spell("Thunder", 20, 80, "black", Fore.YELLOW),
            Spell("Blizzard", 30, 100, "black", Fore.BLUE),
            Spell("Cure", 12, 120, "white", Fore.GREEN)
            ]
        # Create Items
        itemList = self.create_items()
        # Instantiate People
        actions = ["Attack", "Magic", "Items"]
        self.player = Person("""Placeholder""", 460, 65, 60, 34, actions,
                             playerSpells)
        for item in itemList:
            self.player.add_item(item, 5)

        self.enemy = Person("""Shithead""", 460, 65, 60, 34, [], [])
        # Instantiate UI
        self.ui = UI()

    def choose_action(self):
        """Return player action choice."""
        ui = self.ui
        player = self.player
        while True:
            choice = input("Choose an action:")
            if not choice.isdigit():
                ui.print_error("You must select a number")
            elif 1 <= int(choice) <= len(player.action):
                return int(choice) - 1
            else:
                ui.print_error("You must choose a number in the list")

    def choose_spell(self):
        """Return spell choice."""
        ui = self.ui
        player = self.player
        while True:
            choice = input("Choose a spell:")
            if not choice.isdigit():
                ui.print_error("You must enter a number")
            elif int(choice) == len(player.spell) + 1:
                return -1
            elif 1 <= int(choice) <= len(player.spell):
                return int(choice) - 1
            else:
                ui.print_error("You must choose a number in the list")

    def choose_item(self):
        """Return player item choice."""
        ui = self.ui
        player = self.player
        while True:
            choice = input("Choose an Item:")
            if not choice.isdigit():
                ui.print_error("You must enter a number")
            elif int(choice) == len(player.inventory) + 1:
                return -1
            elif 1 <= int(choice) <= len(player.inventory):
                return int(choice) - 1
            else:
                ui.print_error("You must choose a number in the list")

    def battle(self):
        """Begin Battle Phase."""
        ui = self.ui
        player = self.player
        enemy = self.enemy

        while True:
            ui.print_hpmp(player, enemy)
            ui.list_actions(player.action)
            actionIndex = self.choose_action()
            ui.print_selection(player.get_action_name(actionIndex))

            if actionIndex == 0:
                dmg = player.generate_damage()
                enemy.take_damage(dmg)
                ui.print_damage_dealt(player.name, enemy.name, dmg, "attack")

            elif actionIndex == 1:
                ui.list_spells(player.spell)
                spellIndex = self.choose_spell()
                spellName = player.get_spell_name(spellIndex)
                if spellIndex == -1:
                    ui.print_message("You selected Cancel")
                    continue
                ui.print_selection(spellName)
                spellDmg = player.spell[spellIndex].generate_damage()
                if player.get_spell_mp_cost(spellIndex) <= player.get_mp():
                    player.reduce_mp(player.get_spell_mp_cost(spellIndex))
                    if player.spell[spellIndex].type == "white":
                        player.heal(spellDmg)
                        ui.print_healing_done(player.name, player.name,
                                              spellDmg, spellName)
                    elif player.spell[spellIndex].type == "black":
                        enemy.take_damage(spellDmg)
                        ui.print_damage_dealt(player.name, enemy.name,
                                              spellDmg, spellName)
                else:
                    ui.print_error("You do not have enough MP")
                    continue

            elif actionIndex == 2:
                ui.list_inventory(player.inventory)
                itemIndex = self.choose_item()
                if itemIndex == -1:
                    ui.print_message("You selected Cancel")
                    continue
                itemName = player.inventory[itemIndex]["item"].name
                ui.print_selection(itemName)
                itemEffect = player.inventory[itemIndex]["item"].prop
                if player.inventory[itemIndex]["item"].type == "potion":
                    player.heal(itemEffect)
                    ui.print_healing_done(player.name, player.name,
                                          itemEffect, itemName)

            if enemy.get_hp() == 0:
                ui.print_victory("You have won")
                break

            enemyDmg = enemy.generate_damage()
            player.take_damage(enemyDmg)
            ui.print_damage_dealt(enemy.name, player.name, enemyDmg, "attack")

            if player.get_hp() == 0:
                ui.print_defeat("You have died")
                break

    # Create Items
    def create_items(self):
        """Create master Item List."""
        return [
                Item("Potion", "potion", "Heals 50 HP", 50),
                Item("Hi-Potion", "potion", "Heals 100 HP", 100),
                Item("Super Potion", "potion", "Heals 500 HP", 500)
                ]
