import typing

import numpy
import numpy.typing


from game.chuj_constants import ChujConstants
from game.chuj_play import ChujPlay
from game.chuj_player import ChujPlayer
from game.chuj_card import ChujCard


class ChujRound:
    def __init__(self) -> None:
        self.plays: list[ChujPlay] = []
        self.played_cards: list[ChujCard] = []
        self.players: list[ChujPlayer] = []
        self.is_done = False
        self.player_points: typing.Dict[ChujPlayer, int] = {}
        self.player_cards: typing.Dict[ChujPlayer, list[ChujCard]] = {}
        self.points: int = 20

    def play_card(self, card: ChujCard, player: ChujPlayer) -> None:
        if self.is_done:
            raise ValueError("Round is already done")

        if any(c is card for c in self.played_cards):
            raise ValueError(f"Card {card} has already been played in this round")

        if not self.plays or self.plays[-1].is_done:
            self.plays.append(ChujPlay())

        self.plays[-1].play_card(card, player)
        self.played_cards.append(card)

        if len(self.played_cards) == ChujConstants.deck_size:
            self.is_done = True

        if self.plays[-1].is_done:
            if self.plays[-1].taker:
                if self.plays[-1].taker not in self.player_points:
                    self.player_points[self.plays[-1].taker] = 0
                if self.plays[-1].taker not in self.player_cards:
                    self.player_cards[self.plays[-1].taker] = []
                self.player_points[self.plays[-1].taker] += self.plays[-1].points
                self.player_cards[self.plays[-1].taker] += self.plays[-1].played_cards

        if self.is_done:
            if len(self.player_points) == 1:
                taker = list(self.player_points)[0]
                self.player_points[taker] = 0
                for player in self.players:
                    if player is not taker:
                        self.player_points[player] = self.points

            for player in self.players:
                player.points += self.player_points[player]

    def get_played_cards_padded_vector(self) -> numpy.typing.NDArray[numpy.int8]:
        card_indexes = [card.index for card in self.played_cards]
        return numpy.pad(
            numpy.array(card_indexes, dtype=numpy.int8),
            (0, ChujConstants.deck_size - len(card_indexes)),
        )

    def get_taken_cards_padded_vector(
        self, player: ChujPlayer
    ) -> numpy.typing.NDArray[numpy.int8]:
        if player not in self.player_cards:
            return numpy.full(ChujConstants.deck_size, 0, dtype=numpy.int8)
        card_indexes = [card.index for card in self.player_cards[player]]
        return numpy.pad(
            numpy.array(card_indexes, dtype=numpy.int8),
            (0, ChujConstants.deck_size - len(card_indexes)),
        )
