from game.chuj_card import ChujCard
from game.chuj_hand import ChujHand


class ChujPlayer:
    def __init__(self, player_id: str) -> None:
        self.__hand: ChujHand | None = None
        self.points = 0
        self.__player_id = player_id

    @property
    def hand(self) -> ChujHand:
        if not self.__hand:
            raise ValueError("Player has no hand")
        return self.__hand

    @hand.setter
    def hand(self, hand: ChujHand) -> None:
        self.__hand = hand

    @property
    def has_hand(self) -> bool:
        return self.__hand is not None

    @property
    def player_id(self) -> str:
        return self.__player_id

    def play_card(self, card: ChujCard) -> None:
        self.hand.play_card(card)

    def __str__(self):
        return self.__player_id
