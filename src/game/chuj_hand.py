import numpy
import numpy.typing

from game.chuj_card import ChujCard
from game.chuj_constants import ChujConstants


class ChujHand:
    def __init__(self, cards: list[ChujCard]) -> None:
        self.__cards = cards
        self.__is_empty = False

    @property
    def is_empty(self) -> bool:
        return self.__is_empty

    @property
    def available_cards_mask_padded_vector(self) -> numpy.typing.NDArray[numpy.int8]:
        if self.__is_empty:
            raise ValueError("Hand is empty")
        mask = numpy.zeros(ChujConstants.deck_size, dtype=numpy.int8)
        mask[[card.index for card in self.__cards]] = 1
        return mask

    @property
    def available_cards_padded_vector(self) -> numpy.typing.NDArray[numpy.int8]:
        if self.__is_empty:
            raise ValueError("Hand is empty")
        return numpy.pad(
            numpy.array([card.index for card in self.__cards], dtype=numpy.int8),
            (0, ChujConstants.hand_size - len(self.__cards)),
        )

    def play_card(self, card: ChujCard) -> None:
        if card not in self.__cards:
            raise ValueError(f"Card {card} is not in hand")
        self.__cards.remove(card)
        if not self.__cards:
            self.__is_empty = True
