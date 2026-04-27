from game.chuj_card import ChujCard
from game.chuj_hand import ChujHand


class ChujPlayer:
    def __init__(self, hand: ChujHand):
        self.hand = hand
        self.points = 0

    def play_card(self, card: ChujCard):
        self.hand.play_card(card)
