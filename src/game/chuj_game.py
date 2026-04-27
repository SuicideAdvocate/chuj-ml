import numpy

from game.chuj_card import ChujCard
from game.chuj_deck import ChujDeck
from game.chuj_play import ChujPlay
from game.chuj_player import ChujPlayer
from game.chuj_round import ChujRound


class ChujGame:
    max_points = 175

    def __init__(self):
        self.deck = ChujDeck()
        self.is_done = False
        hands = self.deck.get_hands()
        self.players: list[ChujPlayer] = [ChujPlayer(hands[i]) for i in range(4)]
        self.rounds: list[ChujRound] = [ChujRound(self.players)]

    def play_card(self, card: ChujCard, player: ChujPlayer):
        self.rounds[-1].play_card(card, player)
        self.is_done = any(player.points > 100 for player in self.players)

        if not self.is_done and self.rounds[-1].is_done:
            self.rounds.append(ChujRound(self.players))
            hands = self.deck.get_hands()
            for i in range(4):
                self.players[i].hand = hands[i]

    def get_opponent_scores_vector(self, player: ChujPlayer):
        return numpy.array(
            [
                game_player.points
                for game_player in self.players
                if game_player != player
            ],
            dtype=numpy.int16,
        )

    def get_next_player(self):
        if len(self.rounds) == 1:
            # this is the first round
            return self.players[0]
        elif self.rounds[-1].is_done:
            # the lastest round is done
            return self.players[len(self.rounds) % ChujPlay.size]
        elif self.rounds[-1].plays[-1].is_done:
            # the latest play in the latest round is done
            return self.rounds[-1].plays[-1].taker
        else:
            # the play is in progress
            lastest_play_player = self.rounds[-1].plays[-1].players[-1]
            return self.players[self.players.index(lastest_play_player) % ChujPlay.size]
