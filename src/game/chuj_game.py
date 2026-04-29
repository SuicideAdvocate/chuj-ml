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
        self.__round = ChujRound()

        self.advance()

    @property
    def next_player(self) -> ChujPlayer:
        if self.round.is_empty:
            return self.__players[len(self.round.index) % ChujConstants.player_count]
        elif self.round.play.is_empty:
            return self.round.last_taker
        else:
            return self.__players[
                (self.__players.index(self.round.play.last_player) + 1)
                % ChujConstants.player_count
            ]

    def play_card(self, card: ChujCard, player: ChujPlayer) -> None:
        if self.is_done:
            raise ValueError("Game is already done")

        self.__round.play_card(card, player)

        self.__is_done = (
            any(player.points > 100 for player in self.players)
            and self.rounds[-1].is_done
        )

        if self.rounds[-1].is_done and not self.is_done:
            self.deal_cards()

    def get_opponent_scores_vector(
        self, player: ChujPlayer
    ) -> numpy.typing.NDArray[numpy.int16]:
        player_scores = [
            game_player.points for game_player in self.players if game_player != player
        ]
        return numpy.array(
            player_scores,
            dtype=numpy.int16,
        )

    def advance(self) -> None:
        if self.__is_done:
            raise ValueError("Game is already done")

        if not self.round or self.round.is_done:
            self.round = ChujRound()
            for player in self.__players:
                player.hand = ChujHand(self.__deck.next_draw)

        self.round.advance()
