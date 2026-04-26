import enum

import numpy


class Suite(enum.Enum):
    HEARTS = 1,
    BELLS = 2,
    ACORNS = 3,
    LEAVES = 4,


class Value(enum.Enum):
    SEVEN = 1,
    EIGHT = 2,
    NINE = 3,
    TEN = 4,
    UNDER = 5,
    UBER = 6,
    KING = 7,
    ACE = 8,


class Card:
    def __init__(self, suite: Suite, value: Value, points: int, index: int):
        self.suite = suite
        self.value = value
        self.points = points
        self.index = index


class Hand:
    size = 8

    def __init__(self):
        self.cards: list[Card] = []

    def _set_cards(self, cards: list[Card]):
        self.cards = cards

    def play_card(self, card: Card):
        self.cards.remove(card)


class Deck:
    size = 32

    def __init__(self):
        self.cards: list[Card] = []
        for suite in Suite:
            for value in Value:
                points = 0
                if suite is Suite.HEARTS:
                    points = 1
                elif value is Value.UBER:
                    if suite is Suite.ACORNS:
                        points = 4
                    elif suite is Suite.LEAVES:
                        points = 8
                self.cards.append(Card(suite, value, points, len(self.cards) + 1))

    def get_hands(self):
        cards_copy = self.cards.copy()
        numpy.random.shuffle(cards_copy)
        hands: list[Hand] = []
        for _ in range(Play.size):
            hands.append(Hand())
        offset = 0
        for hand in hands:
            hand.cards = cards_copy[offset:offset + hand.size]
            offset += hand.size
        return hands


class Action:
    def __init__(self, card: Card, player: Player):
        self.card = card
        self.player = player


class Play:
    size = 4

    def __init__(self):
        self.actions = numpy.empty(0, dtype=Action)
        self.is_done = False
        self.score = 0
        self.taker: Player | None = None

    def play_card(self, card: Card, player: Player):
        player.play_card(card)

        numpy.append(self.actions, [Action(card, player)])
        self.is_done = len(self.actions) == self.size

        if self.is_done:
            self.score = sum(action.card.points for action in self.actions)
            possible_taker_actions = [action for action in self.actions if
                                      action.card.suite == self.actions[0].card.suite]
            if possible_taker_actions:
                taker_action = max(possible_taker_actions, key=lambda a: a.card.value.value)
                self.taker = taker_action.player
                taker_action.player += self.score


class Round:
    size = 8

    def __init__(self):
        self.plays = numpy.empty(1, dtype=Play)
        self.played_cards = numpy.empty(0, dtype=Card)
        self.is_done = False

    def play_card(self, card: Card, player: Player):
        self.plays[-1].play_card(card, player)
        numpy.append(self.played_cards, [card])

        if len(self.played_cards) == Deck.size:
            self.is_done = True

        if not self.is_done and self.plays[-1].is_done:
            numpy.append(self.plays, [Play()])


class Player:
    def __init__(self):
        self.hand = Hand()
        self.score = 0

    def play_card(self, card: Card):
        self.hand.play_card(card)


class Game:
    max_points = 175

    def __init__(self):
        self.deck = Deck()
        self.players = numpy.full(4, Player())
        self.rounds = numpy.empty(1, dtype=Round)
        self.current_player = self.players[0]
        self.is_done = False

    def play_card(self, card: Card, player: Player):
        self.rounds[-1].play_card(card, player)
        self.is_done = any(player.score > 100 for player in self.players)

        if not self.is_done and self.rounds[-1].is_done:
            numpy.append(self.rounds, [Round()])

    def get_next_player(self):
        if len(self.rounds) == 0:
            # there are no rounds yet
            return self.players[0]
        elif self.rounds[-1].is_done:
            # the lastest round is done
            return self.players[len(self.rounds) % Play.size]
        elif self.rounds[-1].plays[-1].is_done:
            # the latest play in the latest round is done
            return self.rounds[-1].plays[-1].taker
        else:
            # the play is in progress
            lastest_play_player = self.rounds[-1].plays[-1].actions[-1].player
            return self.players[numpy.argwhere(self.players == lastest_play_player)[0] % Play.size]
