import numpy

from src.game.chuj_card import ChujCard
from src.game.chuj_player import ChujPlayer


class ChujPlay:
    size = 4

    def __init__(self):
        self.is_done = False
        self.points = 0
        self.taker: ChujPlayer | None = None
        self.taker_card: ChujCard | None = None
        self.played_cards: list[ChujCard] = []
        self.players: list[ChujPlayer] = []

    def play_card(self, card: ChujCard, player: ChujPlayer):
        # play the card from the hand of the player
        player.play_card(card)
        # add the card to the list of the cards in the play
        # state of the play is observed when making a choice
        self.played_cards.append(card)
        # add the player to the list. this is used to determine the next player
        self.players.append(player)
        # if the number of actions in the play is equal to the size of the play, then the play is done
        self.is_done = len(self.played_cards) == self.size
        # update the play score
        self.points += card.points

        # if there are no played cards, the player is the taker of the play
        if len(self.played_cards) == 1:
            self.taker = player
            self.taker_card = card
        # if there are cards already, taker is changes if current card is the same suite as first card and has higher value
        elif (card.suite == self.played_cards[0].suite
              and self.taker_card
              and card.value.value > self.taker_card.value.value):
            self.taker = player
            self.taker_card = card

    def get_played_cards_padded_vector(self):
        return numpy.pad(numpy.array(card.index for card in self.played_cards),
                         (0, ChujPlay.size - len(self.played_cards)))
