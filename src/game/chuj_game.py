import numpy
import numpy.typing

from game.chuj_constants import ChujConstants
from game.chuj_player import ChujPlayer
from game.chuj_card import ChujCard
from game.chuj_deck import ChujDeck
from game.chuj_round import ChujRound


class ChujGame:
    def __init__(self, players: list[str]):
        if len(players) != 4:
            raise ValueError("There must be exactly 4 players")

        self.deck = ChujDeck()
        self.is_done = False
        self.players = [ChujPlayer(player_id) for player_id in players]
        self.rounds: list[ChujRound] = []
        for player, hand in zip(self.players, self.deck.deal_hands()):
            player.hand = hand

    def play_card(self, card: ChujCard, player: ChujPlayer) -> None:
        if self.is_done:
            raise ValueError("Game is already done")

        if not self.rounds or self.rounds[-1].is_done:
            self.rounds.append(ChujRound())

        self.rounds[-1].play_card(card, player)
        self.is_done = (
            any(player.points > 100 for player in self.players)
            and self.rounds[-1].is_done
        )

        if self.rounds[-1].is_done and not self.is_done:
            for player, hand in zip(self.players, self.deck.deal_hands()):
                player.hand = hand

    def get_opponent_scores_vector(
        self, player: ChujPlayer
    ) -> numpy.typing.NDArray[numpy.int16]:
        player_scores = [
            game_player.points for game_player in self.players if game_player != player
        ]
        return numpy.array(
            player_scores,
            dtype=numpy.int16,
        )

    def get_next_player(self) -> ChujPlayer:
        if not self.rounds or self.rounds[-1].is_done or not self.rounds[-1].plays:
            return self.players[len(self.rounds) % ChujConstants.player_count]
        elif self.rounds[-1].plays[-1].is_done:
            taker = self.rounds[-1].plays[-1].taker
            if not taker:
                raise ValueError("Play is done but has no taker")
            return taker
        else:
            latest_player = self.rounds[-1].plays[-1].players[-1]
            index_of_latest_player = self.players.index(latest_player)
            return self.players[
                (index_of_latest_player + 1) % ChujConstants.player_count
            ]
