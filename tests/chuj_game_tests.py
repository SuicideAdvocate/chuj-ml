import unittest

from src import chuj_game


class GameTests(unittest.TestCase):
    def test_next_player_empty_game(self):
        game = chuj_game.Game()
        next_player = game.get_next_player()
        expected_player = game.players[0]
        self.assertEqual(expected_player, next_player)

    def test_next_player_completed_round(self):
        game = chuj_game.Game()
        game.rounds = [chuj_game.Round()]
        game.rounds[-1].is_done = True
        next_player = game.get_next_player()
        expected_player = game.players[1]
        self.assertEqual(expected_player, next_player)

    def test_next_player_completed_play(self):
        game = chuj_game.Game()
        game.rounds = [chuj_game.Round()]
        game.rounds[-1].plays = [chuj_game.Play()]
        game.rounds[-1].plays[-1].is_done = True
        game.rounds[-1].plays[-1].taker = game.players[2]
        next_player = game.get_next_player()
        expected_player = game.players[2]
        self.assertEqual(expected_player, next_player)

    def test_next_player_incomplete_play(self):
        game = chuj_game.Game()
        card = chuj_game.Card(chuj_game.Suite.HEARTS, chuj_game.Value.SEVEN, 1, 0)
        game.rounds = [chuj_game.Round()]
        game.rounds[-1].plays = [chuj_game.Play()]
        game.rounds[-1].plays[-1].actions = [chuj_game.Action(card, game.players[1])]
        next_player = game.get_next_player()
        expected_player = game.players[2]
        self.assertEqual(expected_player, next_player)


if __name__ == '__main__':
    unittest.main()
