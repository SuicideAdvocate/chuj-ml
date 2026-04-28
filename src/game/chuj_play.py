import numpy
import numpy.typing

from game.chuj_constants import ChujConstants
from game.chuj_player import ChujPlayer
from game.chuj_card import ChujCard


class ChujPlay:
    def __init__(self) -> None:
        self.is_done = False
        self.points = 0
        self.taker: ChujPlayer | None = None
        self.taker_card: ChujCard | None = None
        self.played_cards: list[ChujCard] = []
        self.players: list[ChujPlayer] = []

    def play_card(self, card: ChujCard, player: ChujPlayer) -> None:
        if self.is_done:
            raise ValueError("Play is already done")

        if any(p is player for p in self.players):
            raise ValueError(f"Player {player} has already played in this play")

        if any(c is card for c in self.played_cards):
            raise ValueError(f"Card {card} has already been played in this play")

        player.play_card(card)
        self.played_cards.append(card)
        self.players.append(player)
        self.is_done = len(self.played_cards) == ChujConstants.player_count
        self.points += card.points

        if len(self.played_cards) == 1:
            self.taker = player
            self.taker_card = card
        elif (
            card.suite == self.played_cards[0].suite
            and self.taker_card
            and card.value.value > self.taker_card.value.value
        ):
            self.taker = player
            self.taker_card = card

    def get_played_cards_padded_vector(self) -> numpy.typing.NDArray[numpy.int8]:
        return numpy.pad(
            numpy.array([card.index for card in self.played_cards], dtype=numpy.int8),
            (0, ChujConstants.player_count - len(self.played_cards)),
        )
