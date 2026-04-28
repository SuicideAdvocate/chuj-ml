from operator import contains

import numpy
import numpy.typing

from game.chuj_card import ChujCard
from game.chuj_constants import ChujConstants


class ChujHand:
    def __init__(self, cards: list[ChujCard]) -> None:
        self.cards = cards

    def play_card(self, card: ChujCard) -> None:
        if not contains(self.cards, card):
            raise ValueError(f"Card {card} is not in hand")
        self.cards.remove(card)

    def get_cards_mask_padded_vector(self) -> numpy.typing.NDArray[numpy.int8]:
        mask = numpy.zeros(ChujConstants.deck_size, dtype=numpy.int8)
        mask[[card.index - 1 for card in self.cards]] = 1
        return mask

    def get_cards_padded_vector(self) -> numpy.typing.NDArray[numpy.int8]:
        return numpy.pad(
            numpy.array([card.index for card in self.cards], dtype=numpy.int8),
            (0, ChujConstants.hand_size - len(self.cards)),
        )
