import typing

import numpy


from game.chuj_card import ChujCard
from game.chuj_deck import ChujDeck
from game.chuj_play import ChujPlay
from game.chuj_player import ChujPlayer


class ChujRound:
    size = 8

    def __init__(self, players: list[ChujPlayer]):
        self.plays: list[ChujPlay] = [ChujPlay()]
        self.played_cards: list[ChujCard] = []
        self.players = players
        self.is_done = False
        self.player_points: typing.Dict[ChujPlayer, int] = {}
        self.player_cards: typing.Dict[ChujPlayer, list[ChujCard]] = {}
        self.points: int = 20
        self.is_empty = True

    def play_card(self, card: ChujCard, player: ChujPlayer):
        self.is_empty = False
        # play the card on the play
        self.plays[-1].play_card(card, player)
        # append the played card to the list of played cards in the round
        # this is observed when taking an action
        self.played_cards.append(card)

        if len(self.played_cards) == ChujDeck.size:
            # if the number of played cards equals the deck size, round is done
            self.is_done = True

        if not self.is_done and self.plays[-1].is_done:
            if self.plays[-1].taker:
                # add score of the play to the taker
                self.player_points[self.plays[-1].taker] += self.plays[-1].points
                # add the cards to the player cards this round
                self.player_cards[self.plays[-1].taker] += self.plays[-1].played_cards
            # if the current play is done, but the round is not, append new play to the array of the plays
            self.plays.append(ChujPlay())

        if self.is_done:
            # durch is a situation, where all points were taken by one player
            if len(self.player_points) == 1:
                taker = list(self.player_points)[0]
                # taker receives 0 points
                self.player_points[taker] = 0
                # other receive full points
                for player in self.players:
                    if player is not taker:
                        self.player_points[player] = self.points

            # increment player points by round points for each player
            for player in self.players:
                player.points += self.player_points[player]

    def get_played_cards_padded_vector(self):
        return numpy.pad(
            numpy.array([card.index for card in self.played_cards], dtype=numpy.int16),
            (0, ChujDeck.size - len(self.played_cards)),
        )

    def get_taken_cards_padded_vector(self, player: ChujPlayer):
        if player not in self.player_points:
            return numpy.full(ChujDeck.size, 0)
        return numpy.pad(
            numpy.array(
                [card.index for card in self.player_cards[player]], dtype=numpy.int16
            ),
            (0, ChujDeck.size - len(self.player_cards[player])),
        )
