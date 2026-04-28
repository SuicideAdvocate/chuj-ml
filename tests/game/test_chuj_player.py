import unittest
from unittest.mock import MagicMock

from game.chuj_card import ChujCard, ChujCardSuite, ChujCardValue
from game.chuj_hand import ChujHand
from game.chuj_player import ChujPlayer


class TestChujPlayer(unittest.TestCase):
    def test_initial_points_are_zero(self):
        player = ChujPlayer("p1")
        self.assertEqual(player.points, 0)

    def test_initial_hand_is_none(self):
        player = ChujPlayer("p1")
        self.assertIsNone(player.hand)

    def test_id_is_set(self):
        player = ChujPlayer("player_42")
        self.assertEqual(player.id, "player_42")

    def test_str_returns_id(self):
        player = ChujPlayer("p1")
        self.assertEqual(str(player), "p1")

    def test_play_card_delegates_to_hand(self):
        card = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 1)
        player = ChujPlayer("p1")
        player.hand = MagicMock(spec=ChujHand)
        player.play_card(card)
        player.hand.play_card.assert_called_once_with(card)

    def test_play_card_raises_when_hand_is_none(self):
        card = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 1)
        player = ChujPlayer("p1")
        with self.assertRaises(ValueError):
            player.play_card(card)


if __name__ == "__main__":
    unittest.main()
