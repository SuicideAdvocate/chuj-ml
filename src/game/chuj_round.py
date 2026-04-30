import typing

import numpy
import numpy.typing


from game.chuj_constants import ChujConstants
from game.chuj_play import ChujPlay
from game.chuj_player import ChujPlayer
from game.chuj_card import ChujCard


class ChujRound:
    def __init__(self, index: int, players: list[ChujPlayer]) -> None:
        self.__index = index
        self.__is_empty = True
        self.__is_done = False
        self.__play = ChujPlay(0)
        self.__last_taker: ChujPlayer | None = None
        self.__played_cards: list[ChujCard] = []
        self.__points: int = 0
        self.__player_points: typing.Dict[ChujPlayer, int] = {
            player: 0 for player in players
        }
        self.__players: list[ChujPlayer] = players

    @property
    def index(self) -> int:
        return self.__index

    @property
    def is_empty(self) -> bool:
        return self.__is_empty

    @property
    def is_done(self) -> bool:
        return self.__is_done

    @property
    def play(self) -> ChujPlay:
        return self.__play

    @property
    def last_taker(self) -> ChujPlayer:
        if self.__last_taker is None:
            raise ValueError("Last taker is not set")
        return self.__last_taker

    @property
    def player_points(self) -> typing.Dict[ChujPlayer, int]:
        return self.__player_points

    def play_card(self, card: ChujCard, player: ChujPlayer) -> None:
        if self.is_done:
            raise ValueError("Round is already done")

        if card in self.__played_cards:
            raise ValueError(f"Card {card} has already been played in this round")

        self.__is_empty = False

        self.__play.play_card(card, player)
        if self.play.is_done:
            self.__points += self.play.points
            self.__player_points[self.play.taker] += self.play.points

        self.__played_cards.append(card)
        self.__is_done = len(self.__played_cards) == ChujConstants.deck_size
        if self.is_done:
            players_with_points = [
                p for p, pts in self.__player_points.items() if pts > 0
            ]
            if len(players_with_points) == 1:
                taker = players_with_points[0]
                self.__player_points[taker] = 0
                for player in self.__players:
                    if player is not taker:
                        self.__player_points[player] = self.__points

            for player in self.__players:
                player.points += self.__player_points[player]

    @property
    def played_cards_padded_vector(self) -> numpy.typing.NDArray[numpy.int8]:
        cards_vector = numpy.zeros(ChujConstants.deck_size, dtype=numpy.int8)
        cards_vector[[card.index for card in self.__played_cards]] = 1
        return cards_vector.astype(numpy.int8)

    @property
    def player_points_vector(self) -> numpy.typing.NDArray[numpy.int16]:
        return numpy.array([self.__player_points[player] for player in self.__players])

    def advance(self) -> None:
        if self.is_done:
            raise ValueError("Round is already done")

        if self.__play.is_done:
            self.__play = ChujPlay(self.play.index)
