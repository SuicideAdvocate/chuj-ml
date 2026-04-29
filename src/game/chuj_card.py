import enum


class ChujCardSuite(enum.Enum):
    HEARTS = (1,)
    BELLS = (2,)
    ACORNS = (3,)
    LEAVES = (4,)


class ChujCardValue(enum.Enum):
    SEVEN = (1,)
    EIGHT = (2,)
    NINE = (3,)
    TEN = (4,)
    UNDER = (5,)
    UBER = (6,)
    KING = (7,)
    ACE = (8,)


class ChujCard:
    def __init__(self, suite: ChujCardSuite, value: ChujCardValue, index: int):
        self.__suite = suite
        self.__value = value
        self.__index = index
        special_combinations = {
            (ChujCardSuite.ACORNS, ChujCardValue.UBER): 4,
            (ChujCardSuite.LEAVES, ChujCardValue.UBER): 8,
        }
        self.__points = (
            1
            if suite is ChujCardSuite.HEARTS
            else special_combinations.get((suite, value), 0)
        )

    @property
    def value(self) -> ChujCardValue:
        return self.__value

    @property
    def suite(self) -> ChujCardSuite:
        return self.__suite

    @property
    def index(self) -> int:
        return self.__index

    @property
    def points(self) -> int:
        return self.__points

    def __str__(self) -> str:
        return f"{self.__suite.name} {self.__value.name}"
