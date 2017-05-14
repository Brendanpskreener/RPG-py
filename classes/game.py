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

    def choose_target(self):
        """Placeholder."""
        pass

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

        # Player turn
        # Choose action (every turn)
        #   (choose attack)
        #   Choose spell
        #   Choose item
        # Choose target
        # perform action
        #   spell
        #       reduce mana
        #       logically heal or damage
        #   item
        #       reduce item quantity
        #       logically heal or damage
        # print results
        #   based on item effect, target and value
        #
        # Enemy turn
        #
    def battle(self):
        """Begin Battle Phase."""
        ui = self.ui
        self.playerParty = self.get_party(True)
        self.enemyParty = self.get_party()
        while True:
            ui.print_hpmp(partyMember, enemy)
            for partyMember in self.playerParty:
                ui.list_actions(partyMember.action)
                actionIndex = self.choose_action()
                ui.print_selection(partyMember.get_action_name(actionIndex))
                # Attack
                if actionIndex == 0:
                    self.attack(partyMember, enemy)
                # Spell
                elif actionIndex == 1:
                    ui.list_spells(partyMember.spell)
                    spellIndex = self.choose_spell()
                    if spellIndex == -1:
                        ui.print_message("You selected Cancel")
                        continue
                    spell = partyMember.get_spell(spellIndex)
                    if spell.cost <= partyMember.get_mp():
                        ui.print_selection(partyMember.get_spell_name(spellIndex))
                        self.spell_cast(partyMember, enemy, spell)
                    else:
                        ui.print_error("You do not have enough MP")
                        continue

                # Item
                elif actionIndex == 2:
                    ui.list_inventory(partyMember.inventory)
                    itemIndex = self.choose_item()
                    if itemIndex == -1:
                        ui.print_message("You selected Cancel")
                        continue
                    item = partyMember.get_item(itemIndex)
                    ui.print_selection(item.name)
                    self.use_item(partyMember, partyMember, item)

            if enemy.get_hp() == 0:
                ui.print_victory("You have won")
                break

            # Enemy turn, lol
            self.attack(enemy, partyMember)

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
                "actions": [],
                "spells": []
            })
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
