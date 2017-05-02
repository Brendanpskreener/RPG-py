"""Lists the structure of Spell Class."""
import random


class Spell:
    """Defines the Spell class object."""

    def __init__(self, name, cost, dmg, type, color=None):
        """Shit I have to do for some reason."""
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type
        self.color = color

    def generate_damage(self):
        """Return damage."""
        low = self.dmg - 5
        high = self.dmg + 5
        return random.randrange(low, high)
