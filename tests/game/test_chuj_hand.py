import unittest

import numpy
import numpy.testing

from game.chuj_card import ChujCard, ChujCardSuite, ChujCardValue
from game.chuj_constants import ChujConstants
from game.chuj_hand import ChujHand


class TestChujHand(unittest.TestCase):
    def test_play_card_removes_card_from_hand(self):
        card = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 1)
        hand = ChujHand([card, ChujCard(ChujCardSuite.HEARTS, ChujCardValue.EIGHT, 2)])
        hand.play_card(card)
        self.assertNotIn(card, hand.cards)

    def test_play_card_raises_when_card_not_in_hand(self):
        hand = ChujHand([ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 1)])
        with self.assertRaises(ValueError):
            hand.play_card(ChujCard(ChujCardSuite.HEARTS, ChujCardValue.EIGHT, 2))

    def test_play_card_only_removes_one_instance(self):
        card = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 1)
        hand = ChujHand(
            [
                card,
                ChujCard(ChujCardSuite.HEARTS, ChujCardValue.EIGHT, 2),
                ChujCard(ChujCardSuite.HEARTS, ChujCardValue.NINE, 3),
            ]
        )
        hand.play_card(card)
        self.assertEqual(len(hand.cards), 2)

    def test_get_cards_mask_padded_vector_length(self):
        cards = [
            ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, i)
            for i in range(1, ChujConstants.hand_size + 1)
        ]
        mask = ChujHand(cards).get_cards_mask_padded_vector()
        self.assertEqual(len(mask), ChujConstants.deck_size)

    def test_get_cards_mask_padded_vector_ones_at_card_indexes(self):
        hand = ChujHand(
            [
                ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 1),
                ChujCard(ChujCardSuite.HEARTS, ChujCardValue.EIGHT, 5),
                ChujCard(ChujCardSuite.HEARTS, ChujCardValue.NINE, 32),
            ]
        )
        mask = hand.get_cards_mask_padded_vector()
        numpy.testing.assert_array_equal(mask[[0, 4, 31]], [1, 1, 1])

    def test_get_cards_mask_padded_vector_zeros_elsewhere(self):
        hand = ChujHand([ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 1)])
        mask = hand.get_cards_mask_padded_vector()
        self.assertEqual(mask.sum(), 1)

    def test_get_cards_mask_padded_vector_dtype(self):
        cards = [
            ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, i)
            for i in range(1, ChujConstants.hand_size + 1)
        ]
        mask = ChujHand(cards).get_cards_mask_padded_vector()
        self.assertEqual(mask.dtype, numpy.int8)

    def test_get_cards_padded_vector_length(self):
        cards = [
            ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, i)
            for i in range(1, ChujConstants.hand_size + 1)
        ]
        vec = ChujHand(cards).get_cards_padded_vector()
        self.assertEqual(len(vec), ChujConstants.hand_size)

    def test_get_cards_padded_vector_contains_card_indexes(self):
        hand = ChujHand(
            [
                ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 3),
                ChujCard(ChujCardSuite.HEARTS, ChujCardValue.EIGHT, 7),
                ChujCard(ChujCardSuite.HEARTS, ChujCardValue.NINE, 15),
            ]
        )
        vec = hand.get_cards_padded_vector()
        numpy.testing.assert_array_equal(vec[:3], [3, 7, 15])

    def test_get_cards_padded_vector_pads_with_zeros(self):
        hand = ChujHand([ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 5)])
        vec = hand.get_cards_padded_vector()
        self.assertEqual(len(vec), ChujConstants.hand_size)
        numpy.testing.assert_array_equal(
            vec[1:], numpy.zeros(ChujConstants.hand_size - 1)
        )

    def test_get_cards_padded_vector_dtype(self):
        cards = [
            ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, i)
            for i in range(1, ChujConstants.hand_size + 1)
        ]
        vec = ChujHand(cards).get_cards_padded_vector()
        self.assertEqual(vec.dtype, numpy.int8)


if __name__ == "__main__":
    unittest.main()
