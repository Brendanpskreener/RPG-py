"""Lists the structure of the game class."""
from colorama import Fore, Style
from classes.person import Person
from classes.spell import Spell
from classes.item import Item
from classes.ui import UI
from random import randrange
from random import choice as randChoice


class Game:
    """Defines the Game class object."""

    def __init__(self):
        """Docstring for Game initialization."""
        # Create spell
        self.spellList = [
            Spell("Fire", 10, 60, "black", Fore.RED + Style.BRIGHT),
            Spell("Thunder", 20, 80, "black", Fore.YELLOW),
            Spell("Blizzard", 30, 100, "black", Fore.BLUE),
            Spell("Cure", 12, 120, "white", Fore.GREEN)
            ]
        # Create Items
        self.itemList = self.create_items()
        # Instantiate People
        self.playerParty = []
        self.enemyParty = []
        # Instantiate UI
        self.ui = UI()

    def choose_action(self, player):
        """Return player action choice."""
        ui = self.ui
        ui.list_actions(player.action)
        while True:
            choice = input(f"{player.name}, Choose an action:")
            if not choice.isdigit():
                ui.print_error("You must select a number")
            elif 1 <= int(choice) <= len(player.action):
                i = int(choice) - 1
                ui.print_selection(player.get_action_name(i), player.name)
                return i
            else:
                ui.print_error("You must choose a number in the list")

    def choose_spell(self, player):
        """Return spell object choice.

        Parameters
        ---------
        player : Person
            Person object that will choose a spell from their list of spells
        """
        ui = self.ui
        aSpells = list(filter(lambda s: s.cost <= player.get_mp(),
                              player.spell))
        ui.list_spells(aSpells)
        while True:
            choice = input("Choose a spell:")
            if not choice.isdigit():
                ui.print_error("You must enter a number")
            elif int(choice) == len(aSpells) + 1:
                return None
            elif int(choice)-1 in range(len(aSpells)):
                return aSpells[int(choice) - 1]
            else:
                ui.print_error("You must choose a number in the list")

    def choose_item(self, player):
        """Return player item choice."""
        ui = self.ui
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

    def choose_target(self, party, player):
        """Return target selection.

        Description
        ----------
        Print list of available targets to the console for the player to
        choose from then present the player with a prompt. The choice is
        validated and the result is passed to the UI object to be printed.

        Parameters
        ----------
        party : list
            list of person objects to pick target from
        player : Person
            Person object picking the target
        """
        ui = self.ui
        ui.list_targets(party)
        while True:
            choice = input("Choose a Target:")
            if not choice.isdigit():
                ui.print_error("You must select a number")
            elif 1 <= int(choice) <= len(party):
                i = int(choice) - 1
                ui.print_selection(party[i].name, player.name)
                return i
            elif int(choice) == len(party) + 1:
                return -1
            else:
                ui.print_error("You must choose a number in the list")

    def enemy_choose_action(self, player):
        """Return randomly selected action.

        Description
        -----------
        Result is passed to the UI object to be printed.

        Parameters
        ----------
        player : person
            person object choosing the action
        """
        ui = self.ui
        i = 0
        if any(s.cost <= player.get_mp() for s in player.spell):
            i = randrange(0, 2)
        ui.print_selection(player.get_action_name(i), player.name)
        return i

    def enemy_choose_spell(self, player):
        """Return random spell object.

        Parameters
        ---------
        player : Person
            Person object that will choose a spell from their list of spells
        """
        aSpells = list(filter(lambda s: s.cost <= player.get_mp(),
                              player.spell))
        return randChoice(aSpells)

    def enemy_choose_target(self, party, player):
        """Return "randomly" selected person object.

        Description
        -----------
        Result is passed to the UI object to be printed.

        Parameters
        ----------
        party : list
            list of person objects to choose target from
        player : person
            person object choosing the target
        """
        ui = self.ui
        x = randrange(0, 2)
        if x == 0:
            target = party[randrange(0, len(party))]
            ui.print_selection(target.name, player.name)
            return target
        elif x == 1:
            sortedParty = []
            for index, person in enumerate(party):
                sortedParty.append({"index": index, "hp": person.hp})
            sortedParty.sort(key=lambda x: x["hp"])
            target = party[sortedParty[0]["index"]]
            ui.print_selection(target.name, player.name)
            return target

    def attack(self, source, target):
        """Perform attack action on target."""
        print_damage = self.ui.print_damage_dealt
        print_damage(source.name, target.name,
                     target.take_damage(source.generate_damage()), "attack")

    def spell_cast(self, source, target, spell):
        """Perform spell cast action on target using spell."""
        ui = self.ui
        source.reduce_mp(spell.cost)
        spellDmg = spell.generate_damage()
        if spell.type == "white":
            target.heal(spellDmg)
            ui.print_healing_done(source.name, target.name,
                                  spellDmg, spell.name)
        elif spell.type == "black":
            target.take_damage(spellDmg)
            ui.print_damage_dealt(source.name, target.name,
                                  spellDmg, spell.name)

    def use_item(self, source, target, item):
        """Perform use item action on target with item."""
        ui = self.ui
        if item.type == "potion":
            target.heal(item.value)
            ui.print_healing_done(source.name, target.name,
                                  item.value, item.type)
        source.remove_item(item)

    def perform_player_turn(self):
        """Perform player turn logic."""
        playerParty = self.playerParty
        enemyParty = self.enemyParty
        ui = self.ui
        for partyMember in filter(lambda p: p.hp > 0, playerParty):
            viableEnemy = list(filter(lambda p: p.hp > 0, enemyParty))
            viablePlayer = list(filter(lambda p: p.hp > 0,
                                       playerParty))
            while True:
                ui.print_hpmp(playerParty, True)
                ui.print_hpmp(enemyParty)
                aI = self.choose_action(partyMember)
                # Attack
                if aI == 0:
                    tI = self.choose_target(viableEnemy, partyMember)
                    if tI == -1:
                        ui.print_message("You selected Cancel")
                        continue
                    self.attack(partyMember, enemyParty[tI])
                    break
                # Spell
                elif aI == 1:
                        spell = self.choose_spell(partyMember)
                        if not spell:
                            ui.print_message("You selected Cancel")
                            continue
                        ui.print_selection(spell.name, partyMember.name)
                        if spell.type == "white":
                            party = viablePlayer
                        elif spell.type == "black":
                            party = viableEnemy
                        tI = self.choose_target(party, partyMember)
                        if tI == -1:
                            ui.print_message("You selected Cancel")
                            continue
                        self.spell_cast(partyMember, party[tI], spell)
                        break
                # Item
                elif aI == 2:
                        ui.list_inventory(partyMember.inventory)
                        itemIndex = self.choose_item(partyMember)
                        if itemIndex == -1:
                            ui.print_message("You selected Cancel")
                            continue
                        item = partyMember.get_item(itemIndex)
                        ui.print_selection(item.name, partyMember.name)
                        party = viablePlayer
                        tI = self.choose_target(party, partyMember)
                        if tI == -1:
                            ui.print_message("You selected Cancel")
                            continue
                        self.use_item(partyMember, party[tI], item)
                        break

    def perform_enemy_turn(self):
        """Perform enemy turn logic."""
        playerParty = self.playerParty
        enemyParty = self.enemyParty
        ui = self.ui
        for enemyMember in filter(lambda p: p.hp > 0, enemyParty):
            viableEnemy = list(filter(lambda p: p.hp > 0, enemyParty))
            viablePlayer = list(filter(lambda p: p.hp > 0, playerParty))
            aI = self.enemy_choose_action(enemyMember)
            if aI == 0:
                tar = self.enemy_choose_target(viablePlayer, enemyMember)
                self.attack(enemyMember, tar)
            elif aI == 1:
                spell = self.enemy_choose_spell(enemyMember)
                ui.print_selection(spell.name, enemyMember.name)
                if spell.type == "white":
                    party = viableEnemy
                elif spell.type == "black":
                    party = viablePlayer
                tar = self.enemy_choose_target(party, enemyMember)
                self.spell_cast(enemyMember, tar, spell)

    def check_victory(self):
        """Check for player victory condition."""
        ui = self.ui
        if all(e.get_hp() <= 0 for e in self.enemyParty):
            ui.print_victory("You have won.")
            return True

    def check_defeat(self):
        """Check for player defeat condition."""
        ui = self.ui
        if all(p.get_hp() <= 0 for p in self.playerParty):
            ui.print_defeat("You have lost.")
            return True

    def battle(self):
        """Begin Battle Phase."""
        self.playerParty = self.get_party(True)
        self.enemyParty = self.get_party()
        while True:
            self.perform_player_turn()
            if self.check_victory():
                break
            self.perform_enemy_turn()
            if self.check_defeat():
                break

    # Create Items
    def create_items(self):
        """Create master Item List."""
        return [
                Item("Potion", "potion", "Heals 50 HP", 50),
                Item("Hi-Potion", "potion", "Heals 100 HP", 100),
                Item("Super Potion", "potion", "Heals 500 HP", 500)
                ]

    # Goal: Handle high level player/enemy party creation
    # Player or Enemy party?
    #   If player: get name
    #              add to player list
    #   else: add random number of enemies to enemy list
    #   Tier 1
    def get_party(self, isPlayer=False, count=3):
        """Return party."""
        if isPlayer:
            party = self.get_player_party(count)
        else:
            party = self.get_enemy_party(count)
        return party

    # Tier 2
    # Player Party Creation
    def get_player_party(self, count=3):
        """Return player party."""
        ui = self.ui
        party = []
        for i in range(1, count + 1, 1):
            charName = input(f"Enter player {i} Name:")
            if len(charName) <= 0:
                ui.print_error("You must enter at least 1 character")
            else:
                # Create party member
                partyMember = self.get_person({
                    "name": charName,
                    "hp": 500,
                    "mp": 70,
                    "attack": 45,
                    "defense": 40,
                    "actions": ["Attack", "Magic", "Item"],
                    "spells": self.spellList
                })
                # Fill party member's inventory
                for item in self.itemList:
                    partyMember.add_item(item, 5)
                # Add party member to player party
                self.add_party_member(party, partyMember)
        return party

    # Tier 2
    # Enemy Party Creation
    def get_enemy_party(self, count=3):
        """Return ."""
        party = []
        for i in range(1, count + 1, 1):
            enemy = self.get_person({
                "name": f"Shithead {i}",
                "hp": 500,
                "mp": 70,
                "attack": 45,
                "defense": 40,
                "actions": ["Attack", "Magic", "Item"],
                "spells": self.spellList
            })
            for item in self.itemList:
                enemy.add_item(item, 5)
            self.add_party_member(party, enemy)
        return party

    def get_person(self, stats):
        """Return a person object."""
        # TODO Add stat validation
        return Person(stats)

    # Tier 3
    def add_party_member(self, party, member):
        """Append member to party."""
        if type(member) == Person:
            party.append(member)
        return party

    def remove_party_member(self, party, index):
        """Pop member from party."""
        party.pop(index)
        return party
