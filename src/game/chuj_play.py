import numpy
import numpy.typing

from game.chuj_constants import ChujConstants
from game.chuj_player import ChujPlayer
from game.chuj_card import ChujCard


class ChujPlay:
    def __init__(self) -> None:
        self.__is_done = False
        self.__points = 0
        self.__taker: ChujPlayer | None = None
        self.__taker_card: ChujCard | None = None
        self.__last_player: list[ChujPlayer] = []

    @property
    def is_done(self) -> bool:
        return self.__is_done

    @property
    def points(self) -> int:
        return self.__points

    @property
    def taker(self) -> ChujPlayer:
        if self.__taker is None:
            raise ValueError("Taker is not set")
        return self.__taker

    @property
    def taker_card(self) -> ChujCard:
        if self.__taker_card is None:
            raise ValueError("Taker card is not set")
        return self.__taker_card

    def get_action_mask(self) -> numpy.typing.NDArray[numpy.int8]:
        if not self.played_cards:
            return numpy.ones(32, dtype=numpy.int8)
        first_card_suite_value = self.played_cards[0].suite.value[0] - 1
        return numpy.concatenate(
            [
                numpy.zeros(
                    ChujConstants.hand_size * (first_card_suite_value),
                    dtype=numpy.int8,
                ),
                numpy.ones(ChujConstants.hand_size, dtype=numpy.int8),
                numpy.zeros(
                    ChujConstants.hand_size * (3 - first_card_suite_value),
                    dtype=numpy.int8,
                ),
            ]
        )

    def get_played_cards_padded_vector(self) -> numpy.typing.NDArray[numpy.int8]:
        return numpy.pad(
            numpy.array([card.index for card in self.played_cards], dtype=numpy.int8),
            (0, ChujConstants.player_count - len(self.played_cards)),
        )

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

        if self.taker is None:
            raise ValueError("Taker should not be None when play is done")

        if self.taker_card is None:
            raise ValueError("Taker card should not be None when play is done")
