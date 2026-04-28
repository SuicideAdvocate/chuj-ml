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
        self.suite = suite
        self.value = value
        self.index = index
        _special = {
            (ChujCardSuite.ACORNS, ChujCardValue.UBER): 4,
            (ChujCardSuite.LEAVES, ChujCardValue.UBER): 8,
        }
        self.points = 1 if suite is ChujCardSuite.HEARTS else _special.get((suite, value), 0)

    def __str__(self) -> str:
        return f"{self.suite.name} {self.value.name}"
