"""Lists the structure of the game class."""
from colorama import Fore, Style
from classes.person import Person
from classes.spell import Spell
from classes.item import Item
from classes.ui import UI
from random import randrange
from random import choice as randChoice
from classes.terminalmenu import TerminalMenu


class Game:
    """Defines the Game class object."""

    def __init__(self, ui=UI):
        """Docstring for Game initialization."""
        self.spellList = self.create_spells()
        self.itemList = self.create_items()
        self.playerParty = []
        self.enemyParty = []
        self.ui = ui()
        self.__menu = {}
        # Tier 0
        self.__menu["action"] = TerminalMenu("Choose an action")
        # Tier 1
        self.__menu["attackTarget"] = TerminalMenu("", back=True)
        self.__menu["spell"] = TerminalMenu("", back=True)
        self.__menu["item"] = TerminalMenu("", back=True)
        # Tier 2
        self.__menu["whiteTarget"] = TerminalMenu("", back=True)
        self.__menu["blackTarget"] = TerminalMenu("", back=True)
        self.__menu["goodItemTarget"] = TerminalMenu("", back=True)
        self.__menu["badItemTarget"] = TerminalMenu("", back=True)

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

    def __get_action_menu_options(self, player):
        """Return a list of player action options.

        The player action options list contains a number of option dictionaries
        defining the option's ``text``, ``func``, and optionally its ``args``.
        ``{"text": "foo", "func": bar, "args": ["baz"]}``
        """
        menu = self.__menu
        options = []
        for action in player.action:
            if action == "Attack":
                options.append({"text": action,
                                "func": menu["attackTarget"].serve_menu})
            elif action == "Magic":
                options.append({"text": action,
                                "func": menu["spell"].serve_menu})
            elif action == "Item":
                options.append({"text": action,
                                "func": menu["item"].serve_menu})
        return options

    def __get_spell_menu_options(self, player):
        """Return a list of player spell options.

        The player spell options list contains a number of option dictionaries
        defining the option's ``text``, ``func``, and optionally its ``args``.
        ``{"text": "foo", "func": bar, "args": ["baz"]}``
        """
        options = []
        menu = self.__menu
        for s in filter(lambda s: s.cost <= player.get_mp(), player.spell):
            text = f"{s.color}{s.name}{Style.RESET_ALL} (Cost: {s.cost})"
            if s.type == "black":
                options.append({"text": text,
                                "func": menu["blackTarget"].serve_menu,
                                "args": [s]})
            elif s.type == "white":
                options.append({"text": text,
                                "func": menu["whiteTarget"].serve_menu,
                                "args": [s]})
        return options

    def __get_item_menu_options(self, player):
        """Return a list of player item options.

        The player item options list contains a number of option dictionaries
        defining the option's ``text``, ``func``, and optionally its ``args``.
        ``{"text": "foo", "func": bar, "args": ["baz"]}``
        """
        options = []
        menu = self.__menu
        for i in player.inventory:
            text = f"{i['item'].name} (Quantity: {i['quantity']})"
            if i["item"].type == "potion":
                options.append({"text": text,
                                "func": menu["goodItemTarget"].serve_menu,
                                "args": [i["item"]]})
        return options

    def __get_target_menu_options(self, source, party, func):
        """Return list of menu options ``dict`` containing entities to target.

        Viable targets have more than 0 HP remaining.

        Args:
            source (Person): A person object.
            party (list): A list of person objects.
        """
        viableTargets = []
        for target in party:
            if target.hp > 0:
                viableTargets.append({"text": target.name,
                                      "func": func,
                                      "args": [source, target]})
        return viableTargets

    def __do_attack(self, args):
        source, target = args
        dmg = source.generate_damage()
        return (source.name,
                target.name,
                target.take_damage(dmg),
                "offensive",
                "attack")

    def __do_spell(self, args):
        source, target, spell = args
        source.reduce_mp(spell.cost)
        delta = spell.generate_damage()
        if spell.type == "black":
            deltaType = "offensive"
            hpDelta = target.take_damage(delta)
        if spell.type == "white":
            deltaType = "healing"
            hpDelta = target.heal(delta)
        return (source.name,
                target.name,
                hpDelta,
                deltaType,
                f"{spell.color}{spell.name}{Style.RESET_ALL}")

    def __do_good_item(self, args):
        source, target, item = args
        source.remove_item(item)
        pass

    def perform_player_turn(self):
        """Perform player turn logic."""
        playerParty = self.playerParty
        enemyParty = self.enemyParty
        menu = self.__menu
        ui = self.ui
        for member in filter(lambda p: p.hp > 0, playerParty):
            ui.print_hpmp(playerParty, True)
            ui.print_hpmp(enemyParty)
            print(f"{member.name}'s Turn")
            menu["attackTarget"].options = \
                self.__get_target_menu_options(member, enemyParty,
                                               self.__do_attack)
            # menu["badItemTarget"].options
            menu["goodItemTarget"].options = \
                self.__get_target_menu_options(member, playerParty,
                                               self.__do_good_item)
            menu["blackTarget"].options = \
                self.__get_target_menu_options(member, enemyParty,
                                               self.__do_spell)
            menu["whiteTarget"].options = \
                self.__get_target_menu_options(member, playerParty,
                                               self.__do_spell)
            menu["item"].options = self.__get_item_menu_options(member)
            menu["spell"].options = self.__get_spell_menu_options(member)
            menu["action"].options = self.__get_action_menu_options(member)
            results = menu["action"].serve_menu()
            # print(f"\nRESULTS: {results}\n")
            source, target, hpDelta, deltaType, deltaSource = results

            if deltaType == "offensive":
                ui.print_damage_dealt(source, target, hpDelta, deltaSource)
            elif deltaType == "healing":
                ui.print_healing_done(source, target, hpDelta, deltaSource)

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
        self.playerParty = self.get_player_party(3)
        self.enemyParty = self.get_enemy_party(3)
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
        return [Item("Potion", "potion", "Heals 50 HP", 50),
                Item("Hi-Potion", "potion", "Heals 100 HP", 100),
                Item("Super Potion", "potion", "Heals 500 HP", 500)]

    def create_spells(self):
        """Create master spell list."""
        return [Spell("Fire", 10, 60, "black", Fore.RED + Style.BRIGHT),
                Spell("Thunder", 20, 80, "black", Fore.YELLOW),
                Spell("Blizzard", 30, 100, "black", Fore.BLUE),
                Spell("Cure", 12, 120, "white", Fore.GREEN)]

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
                mbr = Person({
                    "name": charName,
                    "hp": 500,
                    "mp": 70,
                    "attack": 45,
                    "defense": 40,
                    "spells": self.spellList
                })
                mbr.action = ["Attack", "Magic", "Item"]
                # Fill party mbr's inventory
                for item in self.itemList:
                    mbr.add_item(item, 5)
                # Add party mbr to player party
                self.add_party_member(party, mbr)
        return party

    def get_enemy_party(self, count=3):
        """Return ."""
        party = []
        for i in range(1, count + 1, 1):
            enemy = Person({
                "name": f"Shithead {i}",
                "hp": 500,
                "mp": 70,
                "attack": 45,
                "defense": 40,
                "spells": self.spellList
            })
            enemy.action = ["Attack", "Magic", "Item"]
            for item in self.itemList:
                enemy.add_item(item, 5)
            self.add_party_member(party, enemy)
        return party

    def add_party_member(self, party, member):
        """Append member to party."""
        if type(member) == Person:
            party.append(member)
        return party

    def remove_party_member(self, party, index):
        """Pop member from party."""
        party.pop(index)
        return party
