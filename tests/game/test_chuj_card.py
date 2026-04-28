import unittest
import itertools

from game.chuj_card import ChujCard, ChujCardSuite, ChujCardValue


class TestChujCard(unittest.TestCase):
    def test_str_returns_suite_and_value(self):
        for index, (suite, value) in enumerate(
            itertools.product(ChujCardSuite, ChujCardValue)
        ):
            with self.subTest(suite=suite, value=value):
                card = ChujCard(suite, value, index + 1)
                self.assertEqual(str(card), f"{suite.name} {value.name}")

    def test_hearts_cards_have_one_point(self):
        for value in ChujCardValue:
            with self.subTest(value=value):
                card = ChujCard(ChujCardSuite.HEARTS, value, 1)
                self.assertEqual(card.points, 1)

    def test_acorns_uber_has_four_points(self):
        card = ChujCard(ChujCardSuite.ACORNS, ChujCardValue.UBER, 1)
        self.assertEqual(card.points, 4)

    def test_leaves_uber_has_eight_points(self):
        card = ChujCard(ChujCardSuite.LEAVES, ChujCardValue.UBER, 1)
        self.assertEqual(card.points, 8)

    def test_non_scoring_cards_have_zero_points(self):
        non_scoring = [
            (suite, value)
            for suite, value in itertools.product(ChujCardSuite, ChujCardValue)
            if suite is not ChujCardSuite.HEARTS
            and not (
                value is ChujCardValue.UBER
                and suite in (ChujCardSuite.ACORNS, ChujCardSuite.LEAVES)
            )
        ]
        for suite, value in non_scoring:
            with self.subTest(suite=suite, value=value):
                card = ChujCard(suite, value, 1)
                self.assertEqual(card.points, 0)

    def test_index_is_stored(self):
        card = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.TEN, 15)
        self.assertEqual(card.index, 15)

    def test_suite_is_stored(self):
        card = ChujCard(ChujCardSuite.LEAVES, ChujCardValue.KING, 1)
        self.assertEqual(card.suite, ChujCardSuite.LEAVES)

    def test_value_is_stored(self):
        card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.NINE, 1)
        self.assertEqual(card.value, ChujCardValue.NINE)


if __name__ == "__main__":
    unittest.main()
