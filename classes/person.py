"""Lists the structure of Person class."""
import random


class Person:
    """Defines the Person class object."""

    def __init__(self, name, hp, mp, atk, df, action, spell):
        """Shit I have to do for some reason."""
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.action = action
        self.spell = spell
        self.inventory = []

    def attack(self, target):
        """Perform Attack, return damage done."""
        dmg = self.generate_damage()
        target.take_damage(dmg)
        return dmg

    def cast_spell(self, target, spell):
        """Perform spell cast, return spell type and damage."""
        spellDmg = spell.generate_damage()
        if spell.type == "white":
            self.heal(spellDmg)

        elif spell.type == "black":
            target.take_damage(spellDmg)
        return (spell.type, spellDmg)

    def generate_damage(self):
        """Return damage."""
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        """Take Damage."""
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        """Return Heal."""
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

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

    def get_spell_name(self, i):
        """Return spell name."""
        return self.spell[i].name

    def get_spell_mp_cost(self, i):
        """Return spell cost."""
        return self.spell[i].cost

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

    def get_item_name(self, i):
        """Return Item Object's Name."""
        return self.get_item(i).name

    def get_item_quantity(self, i):
        """Return Item Object's quantity within Inventory."""
        return self.inventory[i]["quantity"]
