import numpy
import itertools

from game.chuj_card import ChujCard, ChujCardSuite, ChujCardValue
from game.chuj_constants import ChujConstants


class ChujDeck:
    def __init__(self) -> None:
        self.__cards: list[ChujCard] = []
        self.__draws: list[list[ChujCard]] = []
        for index, (suite, value) in enumerate(
            itertools.product(ChujCardSuite, ChujCardValue)
        ):
            self.__cards.append(ChujCard(suite, value, index))

    @property
    def cards(self) -> list[ChujCard]:
        return self.__cards

    @property
    def next_draw(self) -> list[ChujCard]:
        if not self.__draws:
            numpy.random.shuffle(self.__cards)
            for i in range(ChujConstants.player_count):
                self.__draws.append(
                    self.__cards[
                        i * ChujConstants.hand_size : (i + 1) * ChujConstants.hand_size
                    ]
                )
        return self.__draws.pop(0)
