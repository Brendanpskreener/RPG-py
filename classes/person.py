"""Lists the structure of Person class."""
import random


class Person:
    """Defines the Person class object."""

    def __init__(self, stats):
        """Shit I have to do for some reason."""
        self.name = stats["name"]
        self.maxhp = stats["hp"]
        self.hp = stats["hp"]
        self.maxmp = stats["mp"]
        self.mp = stats["mp"]
        self.atkl = stats["attack"] - 10
        self.atkh = stats["attack"] + 10
        self.df = stats["defense"]
        self.__action = None
        self.spell = stats["spells"]
        self.inventory = []

    def generate_damage(self):
        """Return damage."""
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        """Take Damage."""
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return dmg

    def heal(self, dmg):
        """Return Heal."""
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        return dmg

    def get_hp(self):
        """Return current HP."""
        return self.hp

    def get_max_hp(self):
        """Return max HP."""
        return self.maxhp

    def get_mp(self):
        """Return current MP."""
        return self.mp

    def get_max_mp(self):
        """Return max MP."""
        return self.maxmp

    def reduce_mp(self, cost):
        """Reduce MP."""
        self.mp -= cost

    def get_spell(self, i):
        """Return spell object."""
        return self.spell[i]

    def get_action_name(self, i):
        """Return action name."""
        return self.action[i]

    def add_item(self, newItem, quantity=1):
        """Add quantity to player inventory."""
        for item in self.inventory:
            if newItem == item["item"]:
                item["quantity"] += quantity
                break
        else:
            self.inventory.append({"item": newItem, "quantity": quantity})

    def remove_item(self, oldItem, quantity=1):
        """Remove quantity from player Inventory."""
        for index, item in enumerate(self.inventory):
            if oldItem == item["item"]:
                item["quantity"] -= quantity
                if item["quantity"] <= 0:
                    self.inventory.pop(index)
                break

    def get_item(self, i):
        """Return Item Object from Dictionary within Inventory."""
        return self.inventory[i]["item"]

    def get_item_quantity(self, i):
        """Return Item Object's quantity within Inventory."""
        return self.inventory[i]["quantity"]

    @property
    def action(self):
        """Return self.__action."""
        return self.__action

    @action.setter
    def action(self, value):
        """Set the value of self.__action."""
        if type(value) == list:
            self.__action = value
