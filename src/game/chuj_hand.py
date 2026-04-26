from operator import contains

import numpy

from src.game.chuj_card import ChujCard


class ChujHand:
    size = 8

    def __init__(self):
        self.cards: list[ChujCard] = []

    def play_card(self, card: ChujCard):
        # raise an error if the card is not present in the hand
        if not contains(self.cards, card):
            raise ValueError(f"Card {card} is not in hand")
        # remove the card from the hand by removing it from the array
        self.cards.remove(card)

    def get_cards_padded_vector(self):
        # select index from each of the cards in the hand
        card_indexes = numpy.array(list(card.index for card in self.cards))
        # pad the vector to the hand size with zeros to represent the absence of cards
        return numpy.pad(card_indexes, (0, ChujHand.size - len(self.cards)))
