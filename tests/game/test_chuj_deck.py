import unittest

import numpy

from game.chuj_constants import ChujConstants
from game.chuj_deck import ChujDeck


class TestChujDeck(unittest.TestCase):
    def test_deck_contains_all_cards(self):
        deck = ChujDeck()
        actual_card_indexes = [card.index for card in deck.cards]
        expected_card_indexes = numpy.arange(1, ChujConstants.deck_size + 1).tolist()
        numpy.testing.assert_array_equal(actual_card_indexes, expected_card_indexes)

    def test_hands_contains_all_cards(self):
        deck = ChujDeck()
        hands = deck.deal_hands()
        expected_card_indexes = numpy.arange(1, ChujConstants.deck_size + 1)
        actual_card_indexes = numpy.sort(
            [card.index for hand in hands for card in hand.cards]
        )
        numpy.testing.assert_array_equal(actual_card_indexes, expected_card_indexes)

    def test_hands_are_consistent_with_seed(self):
        deck1 = ChujDeck()
        numpy.random.seed(42)
        hands1 = deck1.deal_hands()

        deck2 = ChujDeck()
        numpy.random.seed(99)
        hands2 = deck2.deal_hands()

        deck3 = ChujDeck()
        numpy.random.seed(42)
        hands3 = deck3.deal_hands()

        deck4 = ChujDeck()
        numpy.random.seed(99)
        hands4 = deck4.deal_hands()

        for h1, h3 in zip(hands1, hands3):
            numpy.testing.assert_array_equal(
                [card.index for card in h1.cards],
                [card.index for card in h3.cards],
            )

        for h2, h4 in zip(hands2, hands4):
            numpy.testing.assert_array_equal(
                [card.index for card in h2.cards],
                [card.index for card in h4.cards],
            )


if __name__ == "__main__":
    unittest.main()
