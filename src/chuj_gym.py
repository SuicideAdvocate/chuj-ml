import functools
from typing import Dict

import gymnasium
import numpy
import pettingzoo
import pettingzoo.utils

from game.chuj_game import ChujGame
from game.chuj_player import ChujPlayer
from game.chuj_constants import ChujConstants


class ChujGym(pettingzoo.AECEnv):
    loss_points = -1000

    metadata = {"render.modes": ["human"], "name": "chuj_gym_v0"}

    def __init__(self, render_mode=None):
        super().__init__()

        self.possible_agents = [
            "agent_" + str(i) for i in range(ChujConstants.player_count)
        ]
        self.agents: list[str] = []

        self.game: ChujGame = ChujGame(self.possible_agents)
        self.agent_to_player_map: Dict[str, ChujPlayer] = {}
        self.render_mode = render_mode
        self.__agent_selector: pettingzoo.utils.AgentSelector = (
            pettingzoo.utils.AgentSelector([])
        )

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return gymnasium.spaces.MultiDiscrete(
            [ChujConstants.max_points + 1]
            # {
            #     "player_score": gymnasium.spaces.Discrete(
            #         ChujConstants.max_points + 1, dtype=numpy.int16
            #     ),
            #     # "opponent_scores": gymnasium.spaces.MultiDiscrete(
            #     #     [ChujGame.max_points + 1] * (ChujPlay.size - 1),
            #     #     dtype=numpy.int16
            #     # ),
            #     # "current_round_played_cards": gymnasium.spaces.MultiDiscrete(
            #     #     [ChujDeck.size + 1] * ChujDeck.size,
            #     #     dtype=numpy.int16),
            #     # "current_play_played_cards": gymnasium.spaces.MultiDiscrete(
            #     #     [ChujDeck.size + 1] * ChujPlay.size,
            #     #     dtype=numpy.int16),
            #     # "curent_round_taken_cards": gymnasium.spaces.MultiDiscrete(
            #     #     [ChujDeck.size + 1] * ChujPlay.size,
            #     #     dtype=numpy.int16),
            #     # "current_hand": gymnasium.spaces.MultiDiscrete(
            #     #     [ChujDeck.size + 1] * ChujHand.size,
            #     #     dtype=numpy.int16),
            # }
        )

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return gymnasium.spaces.Discrete(ChujConstants.deck_size)

    def render(self):
        # TODO render the env
        pass

    def close(self):
        # TODO dispose
        pass

    def observe(self, agent):
        player = self.agent_to_player_map[agent]
        return numpy.array([player.points], dtype=numpy.int16)
        # "opponent_scores": self.game.get_opponent_scores_vector(player),
        # "current_round_played_cards": self.game.rounds[-1].get_played_cards_padded_vector(),
        # "current_play_played_cards": self.game.rounds[-1].plays[-1].get_played_cards_padded_vector(),
        # "curent_round_taken_cards": self.game.rounds[-1].get_taken_cards_padded_vector(player),
        # "current_hand": player.hand.get_cards_padded_vector(),

    def reset(self, seed: int | None = None, options: dict | None = None):
        if seed is not None:
            numpy.random.seed(seed)

        self.agents = self.possible_agents.copy()
        self.game = ChujGame(self.agents)
        self.agent_to_player_map = {
            player.player_id: player for player in self.game.players
        }

        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}

        self.update_agent_selector()
        self.agent_selection = self.__agent_selector.next()
        self.update_action_masks()

    def step(self, action):
        self._cumulative_rewards[self.agent_selection] = 0
        player = self.agent_to_player_map[self.agent_selection]
        card_to_play = next(
            card for card in self.game.deck.cards if card.index == action
        )

        self.game.play_card(card_to_play, player)

        self.terminations = {agent: self.game.is_done for agent in self.agents}

        if self.__agent_selector.is_last():
            self.update_agent_selector()
            if self.game.is_done:
                for player in self.game.players:
                    self.rewards[player.player_id] = (
                        ChujGym.loss_points
                        if player.points > 100
                        else 100 - player.points
                    )
            elif self.game.round.is_done:
                for player in self.game.players:
                    sum_of_opponent_points = sum(
                        points
                        for other_player, points in self.game.round.player_points.items()
                        if other_player != player
                    )
                    self.rewards[player.player_id] = sum_of_opponent_points
            elif self.game.round.play.is_done:
                for player in self.game.players:
                    if player is self.game.round.play.taker:
                        self.rewards[player.player_id] = 0
                    else:
                        self.rewards[player.player_id] = self.game.round.play.points
        else:
            self._clear_rewards()

        self._accumulate_rewards()

        if not self.game.is_done:
            self.agent_selection = self.__agent_selector.next()
            self.game.advance()
            self.update_action_masks()

    def update_agent_selector(self):
        first_agent = self.game.next_player.player_id
        idx = self.agents.index(first_agent)
        shifted_agents = self.agents[idx:] + self.agents[:idx]
        self.__agent_selector = pettingzoo.utils.AgentSelector(shifted_agents)

    def update_action_masks(self):
        current_play_mask = self.game.round.play.action_mask_vector
        for agent in self.agents:
            mask = self.agent_to_player_map[agent].hand.available_cards_vector
            merged_mask = mask & current_play_mask
            if any(m == 1 for m in merged_mask):
                mask = merged_mask
            if not any(m == 1 for m in mask):
                raise ValueError(f"No valid actions for agent {agent}")
            self.infos[agent] = {"action_mask": mask}


def create_env():
    environment = create_raw_env()

    # Recommended wrappers
    # environment = wrappers.OrderEnforcingWrapper(environment)
    # environment = wrappers.AssertOutOfBoundsWrapper(environment)
    # environment = wrappers.CaptureStdoutWrapper(environment)

    return environment


def create_raw_env():
    return ChujGym()
