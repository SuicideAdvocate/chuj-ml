import numpy
import itertools

from game.chuj_card import ChujCard, ChujCardSuite, ChujCardValue
from game.chuj_constants import ChujConstants
from game.chuj_hand import ChujHand


class ChujDeck:
    def __init__(self) -> None:
        self.cards: list[ChujCard] = []
        for index, (suite, value) in enumerate(
            itertools.product(ChujCardSuite, ChujCardValue)
        ):
            self.cards.append(ChujCard(suite, value, index + 1))

    def deal_hands(self) -> list[ChujHand]:
        numpy.random.shuffle(self.cards)
        return [
            ChujHand(
                self.cards[
                    i * ChujConstants.hand_size : (i + 1) * ChujConstants.hand_size
                ]
            )
            for i in range(ChujConstants.player_count)
        ]
