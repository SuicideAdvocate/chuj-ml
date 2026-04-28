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

        self.game: ChujGame | None = None
        self.agent_to_player_map: Dict[str, ChujPlayer] = {}
        self.player_to_agent_map: Dict[ChujPlayer, str] = {}
        self.iteration = 0
        self.render_mode = render_mode

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return gymnasium.spaces.Dict(
            {
                "player_score": gymnasium.spaces.Discrete(
                    ChujConstants.max_points + 1, dtype=numpy.int16
                ),
                # "opponent_scores": gymnasium.spaces.MultiDiscrete(
                #     [ChujGame.max_points + 1] * (ChujPlay.size - 1),
                #     dtype=numpy.int16
                # ),
                # "current_round_played_cards": gymnasium.spaces.MultiDiscrete(
                #     [ChujDeck.size + 1] * ChujDeck.size,
                #     dtype=numpy.int16),
                # "current_play_played_cards": gymnasium.spaces.MultiDiscrete(
                #     [ChujDeck.size + 1] * ChujPlay.size,
                #     dtype=numpy.int16),
                # "curent_round_taken_cards": gymnasium.spaces.MultiDiscrete(
                #     [ChujDeck.size + 1] * ChujPlay.size,
                #     dtype=numpy.int16),
                # "current_hand": gymnasium.spaces.MultiDiscrete(
                #     [ChujDeck.size + 1] * ChujHand.size,
                #     dtype=numpy.int16),
            }
        )

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return gymnasium.spaces.Discrete(ChujConstants.deck_size, start=1)

    def render(self):
        # TODO render the env
        pass

    def close(self):
        # TODO dispose
        pass

    def observe(self, agent):
        player = self.agent_to_player_map[agent]
        return {
            "player_score": player.points,
        }
        # "opponent_scores": self.game.get_opponent_scores_vector(player),
        # "current_round_played_cards": self.game.rounds[-1].get_played_cards_padded_vector(),
        # "current_play_played_cards": self.game.rounds[-1].plays[-1].get_played_cards_padded_vector(),
        # "curent_round_taken_cards": self.game.rounds[-1].get_taken_cards_padded_vector(player),
        # "current_hand": player.hand.get_cards_padded_vector(),

    def reset(self, seed: int | None = None, options: dict | None = None):
        if seed is not None:
            numpy.random.seed(seed)

        self.iteration = 0

        self.agents = self.possible_agents.copy()
        self.game = ChujGame(self.agents)
        self.agent_to_player_map = {
            agent: player
            for player in self.game.players
            for agent in self.agents
            if player.id == agent
        }
        self.player_to_agent_map = {
            player: agent for agent, player in self.agent_to_player_map.items()
        }

        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}

        self.set_next_agent()
        self.update_action_masks()

    def step(self, action):
        self.iteration += 1

        player = self.agent_to_player_map[self.agent_selection]
        card_to_play = [card for card in self.game.deck.cards if card.index == action][
            0
        ]
        self.game.play_card(card_to_play, player)

        self.update_action_masks()
        self.set_next_agent()

        self.terminations = {agent: self.game.is_done for agent in self.agents}

        if self.iteration % 4 == 0:
            for agent in self.agents:
                self.rewards[agent] = 5
            # if self.game.is_done:
            #     for player in self.game.players:
            #         agent = self.player_to_agent_map[player]
            #         self.rewards[agent] = (
            #             ChujGym.loss_points
            #             if player.points > 100
            #             else 100 - player.points
            #         )
            # elif self.game.rounds[-1].is_done:
            #     # if the latest round is done, we reward players based on the points they have dealt
            #     for player in self.game.players:
            #         agent = self.player_to_agent_map[player]
            #         sum_of_opponent_points = sum(
            #             points
            #             for other_player, points in self.game.rounds[-1].player_points
            #             if other_player != player
            #         )
            #         self.rewards[agent] = sum_of_opponent_points
            # else:
            #     for player in self.game.players:
            #         agent = self.player_to_agent_map[player]
            #         if self.game.rounds[-1].plays[-1].taker is player:
            #             self.rewards[agent] = -self.game.rounds[-1].plays[-1].points
            #         else:
            #             self.rewards[agent] = 0

        self._accumulate_rewards()

    def set_next_agent(self):
        next_player = self.game.get_next_player()
        first_agent = self.player_to_agent_map[next_player]
        idx = self.agents.index(first_agent)
        shifted_agents = self.agents[idx:] + self.agents[:idx]
        self._agent_selector = pettingzoo.utils.AgentSelector(shifted_agents)
        self.agent_selection = self._agent_selector.next()

    def update_action_masks(self):
        for agent in self.agents:
            player = self.agent_to_player_map[agent]
            mask = player.hand.get_cards_mask_padded_vector()
            self.infos[agent] = {"action_mask": mask}


def env():
    environment = raw_env()

    # Recommended wrappers
    # environment = wrappers.OrderEnforcingWrapper(environment)
    # environment = wrappers.AssertOutOfBoundsWrapper(environment)
    # environment = wrappers.CaptureStdoutWrapper(environment)

    return environment


def raw_env():
    return ChujGym()
