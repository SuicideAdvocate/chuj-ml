import enum

import gymnasium
import numpy





















max_score = 40


class ChujGym(gymnasium.Env):
    def __init__(self):
        self.deck: Deck = Deck()
        self.player: Player = Player()
        self.remaining_cards: list[Card] = []

        self.action_space = gymnasium.spaces.Discrete(Deck.size)

        self.observation_space = gymnasium.spaces.Dict(
            {  # deck size + 1 for None, play size - 1 since we will be generating random plays for now
                "play": gymnasium.spaces.MultiDiscrete([Deck.size + 1] * Play.size, dtype=numpy.int8),
                # deck size + 1 for None
                "played_cards": gymnasium.spaces.MultiDiscrete([Deck.size + 1] * Deck.size, dtype=numpy.int8),
                # deck size + 1 for None
                "hand": gymnasium.spaces.MultiDiscrete([Deck.size + 1] * Hand.size, dtype=numpy.int8),
            })

    def _get_obs(self):
        return {"play": numpy.array([action.card.index for action in self.player.round.plays[-1].actions] + [0] * (
                Play.size - len(self.player.round.plays[-1].actions)), dtype=numpy.int8),
                "played_cards": numpy.array(
                    [card.index for card in self.player.round.played_cards] + [0] * (
                            Deck.size - len(self.player.round.played_cards)), dtype=numpy.int8),
                "hand": numpy.array(
                    [card.index for card in self.player.hand.cards] + [0] * (Hand.size - len(self.player.hand.cards)),
                    dtype=numpy.int8),
                }

    def _get_info(self):
        return {}

    def reset(self, seed: int | None = None, options: dict | None = None):
        # seed = seed or 512
        super().reset(seed=seed)
        if seed is not None:
            numpy.random.seed(seed)
        hands = self.deck.get_hands()
        self.player = Player()
        self.player.hand = hands[0]
        self.remaining_cards = [card for hand in hands[1:] for card in hand.cards]

        # play 3 random cards in the current play
        for _ in range(3):
            card_to_play = numpy.random.choice(self.remaining_cards)
            # foku me, but the sample works so whatever
            self.player.round.play_card(card_to_play, Player())
            self.remaining_cards.remove(card_to_play)

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action: int):
        # selected card does not necessarily exist on players hand
        # action masking should be applied here, but for now we just punish this action by giving a negative reward
        selected_card = next(card for card in self.deck.cards if card.index == action + 1)

        # play 3 random cards in the current play
        for _ in range(3):
            card_to_play = numpy.random.choice(self.remaining_cards)
            # foku me, but the sample works so whatever
            self.player.round.play_card(card_to_play, Player())
            self.remaining_cards.remove(card_to_play)

        # check, if player has the card on hand
        # if player picked an invalid card, do a large negative score
        # and terminate the episode
        if selected_card not in self.player.hand.cards:
            observation = self._get_obs()
            info = self._get_info()
            reward = -1000
            terminated = True
            truncated = False

            return observation, reward, terminated, truncated, info

        self.player.play_card(selected_card)

        score = 0
        # find an action that takes the round
        if self.player.round.plays[-1].taker is self.player:
            score = self.player.round.plays[-1].score

        observation = self._get_obs()
        info = self._get_info()
        reward = score * -1
        terminated = len(self.player.hand.cards) == 0
        truncated = False

        return observation, reward, terminated, truncated, info
