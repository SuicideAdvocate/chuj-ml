import numpy

from game.chuj_card import ChujCard, ChujCardSuite, ChujCardValue
from game.chuj_hand import ChujHand
from game.chuj_play import ChujPlay


class ChujDeck:
    size = 32

    def __init__(self):
        self.cards: list[ChujCard] = []
        index = 0
        for suite in ChujCardSuite:
            for value in ChujCardValue:
                points = 0
                if suite is ChujCardSuite.HEARTS:
                    points = 1
                elif value is ChujCardValue.UBER:
                    if suite is ChujCardSuite.ACORNS:
                        points = 4
                    elif suite is ChujCardSuite.LEAVES:
                        points = 8
                # index is offset here by one, since 0 represents the absence of a card in vector
                self.cards.append(ChujCard(suite, value, points, index + 1))
                index += 1

    def get_hands(self):
        # shuffle the cards to deal random hands
        numpy.random.shuffle(self.cards)
        # prepare 4 hands to deal cards
        hands = [ChujHand() for _ in range(ChujPlay.size)]
        # offset to keep track of where we are in the deck when dealing cards to hands
        offset = 0
        for hand in hands:
            # set cards for hand from offset to the hand size
            hand.cards = self.cards[offset : offset + ChujHand.size]
            # move the offset for the next hand
            offset += ChujHand.size
        return hands
