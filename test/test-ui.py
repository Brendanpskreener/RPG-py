"""Test classes.ui."""
from classes.ui import UI
from classes.person import Person
import unittest

class TestUI(unittest.TestCase):
    """Testing the Ui Class."""

    def setUp(self):
        """Instantiate a new UI object."""
        self.ui = UI()

    def tearDown(self):
        """Delete UI object."""

    def test_ui_class_instantiates_ui_object(self):
        """UI Class instantiates a ui object."""
        self.assertEqual(type(self.ui), UI, "Does not create a ui object")

    def test_ui_print_hpmp(self):
        """ui.print_hpmp prints to a string console."""
        def write(value):
            return value

        player = Person("test0", 200, 100, 10, 10, [], [])
        enemy = Person("test1", 200, 100, 10, 10, [], [])
        self.assertEqual(type(self.ui.print_hpmp(player, enemy, write)), str,
                         "Does not print a string.")
