import unittest
import unittest.mock

import numpy

from src.game.chuj_card import ChujCard, ChujCardSuite, ChujCardValue
from src.game.chuj_hand import ChujHand


class TestChujHand(unittest.TestCase):
    def test_play_card_removes_card(self):
        card_to_remove = unittest.mock.MagicMock(spec=ChujCard)
        card_to_keep = unittest.mock.MagicMock(spec=ChujCard)
        hand = ChujHand()
        hand.cards = [card_to_remove, card_to_keep]
        hand.play_card(card_to_remove)
        numpy.testing.assert_array_equal(hand.cards, [card_to_keep])

    def test_play_card_raises_error(self):
        card_to_remove = unittest.mock.MagicMock(spec=ChujCard)
        hand = ChujHand()
        hand.cards = []
        with self.assertRaises(ValueError):
            hand.play_card(card_to_remove)

    def test_get_padded_vector_empty(self):
        hand = ChujHand()
        expected_vector = numpy.full(ChujHand.size, 0)
        actual_vector = hand.get_cards_padded_vector()
        numpy.testing.assert_array_equal(actual_vector, expected_vector)

    def test_get_padded_vector_full(self):
        hand = ChujHand()
        hand.cards = numpy.full(ChujHand.size, ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 1, 1)).tolist()
        expected_vector = numpy.full(ChujHand.size, 1)
        actual_vector = hand.get_cards_padded_vector()
        numpy.testing.assert_array_equal(actual_vector, expected_vector)

    def test_get_padded_vector_partial(self):
        hand = ChujHand()
        hand.cards = numpy.full(ChujHand.size - 4, ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 1, 1)).tolist()
        expected_vector = numpy.concatenate((numpy.full(ChujHand.size - 4, 1), numpy.full(4, 0)))
        actual_vector = hand.get_cards_padded_vector()
        numpy.testing.assert_array_equal(actual_vector, expected_vector)


if __name__ == '__main__':
    unittest.main()
