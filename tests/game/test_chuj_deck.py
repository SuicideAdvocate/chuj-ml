import unittest

import numpy

from game.chuj_deck import ChujDeck


class TestChujDeck(unittest.TestCase):
    def test_deck_contains_all_cards(self):
        deck = ChujDeck()
        actual_card_indexes = [card.index for card in deck.cards]
        expected_card_indexes = numpy.arange(1, ChujDeck.size + 1).tolist()
        numpy.testing.assert_array_equal(actual_card_indexes, expected_card_indexes)

    def test_hands_contains_all_cards(self):
        deck = ChujDeck()
        hands = deck.get_hands()
        expected_card_indexes = numpy.arange(1, ChujDeck.size + 1)
        actual_card_indexes = numpy.sort([card.index for hand in hands for card in hand.cards])
        numpy.testing.assert_array_equal(actual_card_indexes, expected_card_indexes)

    def test_hands_are_consistent_with_seed(self):
        deck1 = ChujDeck()
        numpy.random.seed(42)
        hands1 = deck1.get_hands()
        deck2 = ChujDeck()
        numpy.random.seed(99)
        hands2 = deck2.get_hands()
        numpy.random.seed(42)
        deck3 = ChujDeck()
        hands3 = deck3.get_hands()
        numpy.random.seed(99)
        deck4 = ChujDeck()
        hands4 = deck4.get_hands()
        for hand1, hand3 in zip(hands1, hands3):
            actual_card_indexes1 = numpy.array([card.index for card in hand1.cards])
            actual_card_indexes3 = numpy.array([card.index for card in hand3.cards])
            numpy.testing.assert_array_equal(actual_card_indexes1, actual_card_indexes3)

        for hand2, hand4 in zip(hands2, hands4):
            actual_card_indexes2 = numpy.array([card.index for card in hand2.cards])
            actual_card_indexes4 = numpy.array([card.index for card in hand4.cards])
            numpy.testing.assert_array_equal(actual_card_indexes2, actual_card_indexes4)


if __name__ == '__main__':
    unittest.main()
