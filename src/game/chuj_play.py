import numpy
import numpy.typing

from game.chuj_constants import ChujConstants
from game.chuj_player import ChujPlayer
from game.chuj_card import ChujCard, ChujCardSuite


class ChujPlay:
    def __init__(self) -> None:
        self.__is_empty = True
        self.__is_done = False
        self.__points = 0
        self.__taker: ChujPlayer | None = None
        self.__taker_card: ChujCard | None = None
        self.__last_player: ChujPlayer | None = None
        self.__played_cards: list[ChujCard] = []

    @property
    def last_player(self) -> ChujPlayer:
        if self.__last_player is None:
            raise ValueError("Last player is not set")
        return self.__last_player

    @property
    def is_empty(self) -> bool:
        return self.__is_empty

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
    def action_mask_vector(self) -> numpy.typing.NDArray[numpy.int8]:
        if not self.__played_cards:
            return numpy.full(ChujConstants.deck_size, 1, dtype=numpy.int8)
        first_card_suite_value = self.__played_cards[0].suite.value[0] - 1
        return numpy.concatenate(
            [
                numpy.full(
                    ChujConstants.hand_size * first_card_suite_value,
                    0,
                    dtype=numpy.int8,
                ),
                numpy.full(ChujConstants.hand_size, 1, dtype=numpy.int8),
                numpy.full(
                    ChujConstants.hand_size * (3 - first_card_suite_value),
                    0,
                    dtype=numpy.int8,
                ),
            ]
        )

    @property
    def played_cards_vector(self) -> numpy.typing.NDArray[numpy.int8]:
        cards_vector = numpy.zeros(ChujConstants.deck_size, dtype=numpy.int8)
        cards_vector[[card.index for card in self.__played_cards]] = 1
        return cards_vector.astype(numpy.int8)

    def play_card(self, card: ChujCard, player: ChujPlayer) -> None:
        if self.is_done:
            raise ValueError("Play is already done")

        if any(c is card for c in self.__played_cards):
            raise ValueError(f"Card {card} has already been played in this play")

        player.play_card(card)
        self.__is_empty = False
        self.__played_cards.append(card)
        self.__last_player = player
        self.__is_done = len(self.__played_cards) == ChujConstants.player_count
        self.__points += card.points

        if len(self.__played_cards) == 1 or (
            card.suite == self.__played_cards[0].suite
            and self.__taker_card
            and card.value.value > self.__taker_card.value.value
        ):
            self.__taker = player
            self.__taker_card = card
