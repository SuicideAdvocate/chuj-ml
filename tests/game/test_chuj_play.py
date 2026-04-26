import unittest
import unittest.mock

import numpy

from src.game.chuj_card import ChujCard, ChujCardSuite, ChujCardValue
from src.game.chuj_play import ChujPlay
from src.game.chuj_player import ChujPlayer


class TestChujPlay(unittest.TestCase):
    def test_play_card_taker_is_correct(self):
        card1 = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 1, 1)
        card2 = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.EIGHT, 1, 2)
        card3 = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.NINE, 1, 3)
        card4 = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.TEN, 1, 4)
        expected_taker = ChujPlayer()
        expected_taker.play_card = unittest.mock.MagicMock()
        other_player = ChujPlayer()
        other_player.play_card = unittest.mock.MagicMock()
        play = ChujPlay()
        play.play_card(card1, other_player)
        play.play_card(card2, other_player)
        play.play_card(card3, other_player)
        play.play_card(card4, expected_taker)
        self.assertTrue(play.is_done)
        self.assertEqual(play.points, 4)
        self.assertEqual(play.taker, expected_taker)
        numpy.testing.assert_array_equal(play.played_cards, [card1, card2, card3, card4])
        other_player.play_card.assert_has_calls(
            [unittest.mock.call(card1), unittest.mock.call(card2), unittest.mock.call(card3)])
        expected_taker.play_card.assert_called_once_with(card4)


if __name__ == '__main__':
    unittest.main()
