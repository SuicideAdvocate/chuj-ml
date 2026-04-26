import unittest
import unittest.mock

from src.game.chuj_hand import ChujHand
from src.game.chuj_player import ChujPlayer


class TestChujPlayer(unittest.TestCase):
    def test_play_card(self):
        card = unittest.mock.MagicMock()
        player = ChujPlayer()
        hand = ChujHand()
        hand.play_card = unittest.mock.MagicMock()
        player.hand = hand
        player.play_card(card)

        hand.play_card.assert_called_once_with(card)


if __name__ == '__main__':
    unittest.main()
