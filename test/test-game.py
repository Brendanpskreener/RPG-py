"""classes.game unit tests."""
import unittest
from classes.game import Game


class TestGameMethods(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.enemyParty = self.game.get_enemy_party(3)
        self.game.playerParty = self.game.get_enemy_party(1)

    def test_enemy_choose_action(self):
        game = self.game
        player = game.enemyParty[0]
        self.assertEqual(type(game.enemy_choose_action(player)), int)
        with self.assertRaises(TypeError):
            game.enemy_choose_action()
        player.action = []
        with self.assertRaises(IndexError):
            game.enemy_choose_action(player)

    def test_get_attack_target_menu_options(self):
        game = self.game
        party = game.enemyParty
        source = game.playerParty[0]
        self.assertEqual(
            type(game._Game__get_attack_target_menu_options(source, party)),
            list
        )
        self.assertEqual(
            type(game._Game__get_attack_target_menu_options(source, party)[0]),
            dict
        )
        self.assertTrue(
            "text" in game._Game__get_attack_target_menu_options(source, party)[0]
        )
        self.assertTrue(
            "func" in game._Game__get_attack_target_menu_options(source, party)[0]
        )
        self.assertTrue(
            "args" in game._Game__get_attack_target_menu_options(source, party)[0]
        )
        self.assertEqual(
            len(game._Game__get_attack_target_menu_options(source, party)[0]["args"]),
            2
        )


if __name__ == "__main__":
    unittest.main()
