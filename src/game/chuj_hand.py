import numpy
import numpy.typing

from game.chuj_card import ChujCard
from game.chuj_constants import ChujConstants


class ChujHand:
    def __init__(self, cards: list[ChujCard]) -> None:
        self.__cards = cards
        self.__is_empty = False

    def cards(self) -> ChujHand:
        return ChujHand(self.__cards)

    @property
    def is_empty(self) -> bool:
        return self.__is_empty

    @property
    def available_cards_vector(self) -> numpy.typing.NDArray[numpy.int8]:
        if self.__is_empty:
            raise ValueError("Hand is empty")
        cards_vector = numpy.zeros(ChujConstants.deck_size, dtype=numpy.int8)
        cards_vector[[card.index for card in self.__cards]] = 1
        return cards_vector.astype(numpy.int8)

    def play_card(self, card: ChujCard) -> None:
        if card not in self.__cards:
            raise ValueError(f"Card {card} is not in hand")
        self.__cards.remove(card)
        if not self.__cards:
            self.__is_empty = True
