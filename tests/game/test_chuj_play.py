import unittest
from unittest.mock import MagicMock

import numpy
import numpy.testing

from game.chuj_card import ChujCard, ChujCardSuite, ChujCardValue
from game.chuj_constants import ChujConstants
from game.chuj_hand import ChujHand
from game.chuj_play import ChujPlay
from game.chuj_player import ChujPlayer


class TestChujPlay(unittest.TestCase):
    def test_initial_state_is_not_done(self):
        play = ChujPlay()
        self.assertFalse(play.is_done)

    def test_initial_points_are_zero(self):
        play = ChujPlay()
        self.assertEqual(play.points, 0)

    def test_initial_taker_is_none(self):
        play = ChujPlay()
        self.assertIsNone(play.taker)

    def test_initial_taker_card_is_none(self):
        play = ChujPlay()
        self.assertIsNone(play.taker_card)

    def test_play_card_calls_player_play_card(self):
        card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 1)
        player = MagicMock(spec=ChujPlayer)
        ChujPlay().play_card(card, player)
        player.play_card.assert_called_once_with(card)

    def test_first_played_card_sets_taker(self):
        card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 1)
        player = MagicMock(spec=ChujPlayer)
        play = ChujPlay()
        play.play_card(card, player)
        self.assertIs(play.taker, player)

    def test_first_played_card_sets_taker_card(self):
        card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 1)
        player = MagicMock(spec=ChujPlayer)
        play = ChujPlay()
        play.play_card(card, player)
        self.assertIs(play.taker_card, card)

    def test_higher_same_suite_card_takes_over_taker(self):
        card_low = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 1)
        card_high = ChujCard(ChujCardSuite.BELLS, ChujCardValue.ACE, 2)
        p1 = MagicMock(spec=ChujPlayer)
        p2 = MagicMock(spec=ChujPlayer)
        play = ChujPlay()
        play.play_card(card_low, p1)
        play.play_card(card_high, p2)
        self.assertIs(play.taker, p2)

    def test_lower_same_suite_card_does_not_take_over_taker(self):
        card_high = ChujCard(ChujCardSuite.BELLS, ChujCardValue.ACE, 1)
        card_low = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 2)
        p1 = MagicMock(spec=ChujPlayer)
        p2 = MagicMock(spec=ChujPlayer)
        play = ChujPlay()
        play.play_card(card_high, p1)
        play.play_card(card_low, p2)
        self.assertIs(play.taker, p1)

    def test_different_suite_card_does_not_take_over_taker(self):
        card_first = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 1)
        card_other = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.ACE, 2)
        p1 = MagicMock(spec=ChujPlayer)
        p2 = MagicMock(spec=ChujPlayer)
        play = ChujPlay()
        play.play_card(card_first, p1)
        play.play_card(card_other, p2)
        self.assertIs(play.taker, p1)

    def test_points_accumulate_for_each_card(self):
        card1 = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.SEVEN, 1)
        card2 = ChujCard(ChujCardSuite.HEARTS, ChujCardValue.EIGHT, 2)
        play = ChujPlay()
        play.play_card(card1, MagicMock(spec=ChujPlayer))
        play.play_card(card2, MagicMock(spec=ChujPlayer))
        self.assertEqual(play.points, 2)

    def test_is_done_after_all_players_play(self):
        play = ChujPlay()
        for i in range(1, ChujConstants.player_count + 1):
            card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, i)
            play.play_card(card, MagicMock(spec=ChujPlayer))
        self.assertTrue(play.is_done)

    def test_is_not_done_before_all_players_play(self):
        card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 1)
        play = ChujPlay()
        play.play_card(card, MagicMock(spec=ChujPlayer))
        self.assertFalse(play.is_done)

    def test_play_card_raises_when_play_is_done(self):
        play = ChujPlay()
        for i in range(1, ChujConstants.player_count + 1):
            card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, i)
            play.play_card(card, MagicMock(spec=ChujPlayer))
        extra_card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.EIGHT, 99)
        with self.assertRaises(ValueError):
            play.play_card(extra_card, MagicMock(spec=ChujPlayer))

    def test_play_card_raises_when_player_already_played(self):
        card1 = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 1)
        card2 = ChujCard(ChujCardSuite.BELLS, ChujCardValue.EIGHT, 2)
        player = MagicMock(spec=ChujPlayer)
        play = ChujPlay()
        play.play_card(card1, player)
        with self.assertRaises(ValueError):
            play.play_card(card2, player)

    def test_play_card_raises_when_card_already_played(self):
        card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 1)
        play = ChujPlay()
        play.play_card(card, MagicMock(spec=ChujPlayer))
        with self.assertRaises(ValueError):
            play.play_card(card, MagicMock(spec=ChujPlayer))

    def test_get_played_cards_padded_vector_length(self):
        card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 1)
        play = ChujPlay()
        play.play_card(card, MagicMock(spec=ChujPlayer))
        vec = play.get_played_cards_padded_vector()
        self.assertEqual(len(vec), ChujConstants.player_count)

    def test_get_played_cards_padded_vector_contains_card_indexes(self):
        card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 7)
        play = ChujPlay()
        play.play_card(card, MagicMock(spec=ChujPlayer))
        vec = play.get_played_cards_padded_vector()
        self.assertEqual(vec[0], 7)

    def test_get_played_cards_padded_vector_pads_with_zeros(self):
        card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 7)
        play = ChujPlay()
        play.play_card(card, MagicMock(spec=ChujPlayer))
        vec = play.get_played_cards_padded_vector()
        numpy.testing.assert_array_equal(
            vec[1:], numpy.zeros(ChujConstants.player_count - 1)
        )

    def test_get_played_cards_padded_vector_dtype(self):
        card = ChujCard(ChujCardSuite.BELLS, ChujCardValue.SEVEN, 1)
        play = ChujPlay()
        play.play_card(card, MagicMock(spec=ChujPlayer))
        vec = play.get_played_cards_padded_vector()
        self.assertEqual(vec.dtype, numpy.int8)


if __name__ == "__main__":
    unittest.main()
