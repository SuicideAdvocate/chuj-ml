import enum


class ChujCardSuite(enum.Enum):
    HEARTS = 1,
    BELLS = 2,
    ACORNS = 3,
    LEAVES = 4,


class ChujCardValue(enum.Enum):
    SEVEN = 1,
    EIGHT = 2,
    NINE = 3,
    TEN = 4,
    UNDER = 5,
    UBER = 6,
    KING = 7,
    ACE = 8,


class ChujCard:
    def __init__(self, suite: ChujCardSuite, value: ChujCardValue, points: int, index: int):
        self.suite = suite
        self.value = value
        self.points = points
        self.index = index
