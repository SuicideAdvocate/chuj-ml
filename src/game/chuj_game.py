import numpy
import numpy.typing

from game.chuj_constants import ChujConstants
from game.chuj_hand import ChujHand
from game.chuj_player import ChujPlayer
from game.chuj_card import ChujCard
from game.chuj_deck import ChujDeck
from game.chuj_round import ChujRound


class ChujGame:
    def __init__(self, players_ids: list[str]):
        if len(players_ids) != 4:
            raise ValueError("There must be exactly 4 players")

        self.__deck = ChujDeck()
        self.__is_done = False
        self.__players = [ChujPlayer(player_id) for player_id in players_ids]
        self.__round = ChujRound(0, self.__players)

        self.advance()

    @property
    def round(self) -> ChujRound:
        return self.__round

    @property
    def is_done(self) -> bool:
        return self.__is_done

    @property
    def deck(self) -> ChujDeck:
        return self.__deck

    @property
    def players(self) -> list[ChujPlayer]:
        return self.__players

    @property
    def next_player(self) -> ChujPlayer:
        if self.__round.is_empty:
            return self.__players[self.__round.index % ChujConstants.player_count]
        elif self.__round.play.is_empty:
            return self.__round.last_taker
        else:
            return self.__players[
                (self.__players.index(self.__round.play.last_player) + 1)
                % ChujConstants.player_count
            ]

    def play_card(self, card: ChujCard, player: ChujPlayer) -> None:
        if self.__is_done:
            raise ValueError("Game is already done")

        self.__round.play_card(card, player)

        self.__is_done = (
            any(player.points > 100 for player in self.__players)
            and self.__round.is_done
        )

    @property
    def player_scores_vector(self) -> numpy.typing.NDArray[numpy.int16]:
        return numpy.array(
            [game_player.points for game_player in self.__players],
            dtype=numpy.int16,
        )

    def advance(self) -> None:
        if self.__is_done:
            raise ValueError("Game is already done")

        if not self.__round or self.__round.is_done:
            self.__round = ChujRound(self.__round.index + 1, self.__players)

        for player in self.__players:
            if not player.has_hand or player.hand.is_empty:
                player.hand = ChujHand(self.__deck.next_draw)

        self.__round.advance()
