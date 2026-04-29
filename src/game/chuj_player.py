from game.chuj_card import ChujCard
from game.chuj_hand import ChujHand


class ChujPlayer:
    def __init__(self, id: str) -> None:
        self.hand: ChujHand | None = None
        self.__points = 0
        self.__id = id

    @property
    def id(self) -> str:
        return self.__id

    @property
    def points(self) -> int:
        return self.__points

    def play_card(self, card: ChujCard) -> None:
        if not self.hand:
            raise ValueError("Player has no hand")
        self.hand.play_card(card)

    def __str__(self):
        return self.id
