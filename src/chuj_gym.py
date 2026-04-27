import functools
from typing import Dict

import gymnasium
import numpy
import pettingzoo

from game.chuj_deck import ChujDeck
from game.chuj_game import ChujGame
from game.chuj_play import ChujPlay
from game.chuj_player import ChujPlayer


class ChujGym(pettingzoo.AECEnv):
    loss_points = -1000

    metadata = {"render.modes": ["human"], "name": "chuj_gym_v0"}

    def __init__(self, render_mode=None):
        super().__init__()

        self.possible_agents = ["agent_" + str(i) for i in range(ChujPlay.size)]
        self.agents: list[str] = []

        self.game: ChujGame = ChujGame()
        self.agent_to_player_map: Dict[str, ChujPlayer] = {}
        self.player_to_agent_map: Dict[ChujPlayer, str] = {}
        self.iteration = 0
        self.render_mode = render_mode
        self.infos = {agent: {} for agent in self.agents}

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return gymnasium.spaces.Dict(
            {
                "player_score": gymnasium.spaces.Discrete(
                    ChujGame.max_points + 1, dtype=numpy.int16
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
        return gymnasium.spaces.Discrete(ChujDeck.size, start=1)

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

        self.game = ChujGame()
        self.iteration = 0

        self.agents = self.possible_agents.copy()
        self.agent_to_player_map = {
            agent: self.game.players[i] for i, agent in enumerate(self.agents)
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

    def update_action_masks(self):
        for agent in self.agents:
            player = self.agent_to_player_map[agent]
            mask = numpy.full(ChujDeck.size, 0, dtype=numpy.int8)
            for index in player.hand.get_card_indexes():
                mask[index - 1] = 1
            self.infos[agent] = {"action_mask": mask}

    def step(self, action):
        # increment the iteration to keep track of the current step in the game
        self.iteration += 1

        # select the next player
        next_player = self.game.get_next_player()

        # play a card based on the next player decision to move the environment
        card_to_play = [card for card in self.game.deck.cards][0]
        self.game.play_card(card_to_play, next_player)

        self.update_action_masks()
        self.set_next_agent()

        # if there are 4 iterations, it means all agents have had a turn and we can distribute rewards
        if self.iteration == 4:
            # reset the iteration for the next round of steps
            self.iteration = 0

            # assign rewards to the players
            if self.game.is_done:
                # if the game is done, assign rewards based on the final scores
                # losers get negative rewards, while the survivors get reward based on how far from 100 points they are
                for player in self.game.players:
                    agent = self.player_to_agent_map[player]
                    self.rewards[agent] = (
                        ChujGym.loss_points
                        if player.points > 100
                        else 100 - player.points
                    )
            elif self.game.rounds[-1].is_empty:
                # if the latest round is empty, we one round before that has just been completed
                # we reward players with points, they have avoided
                for player in self.game.players:
                    agent = self.player_to_agent_map[player]
                    self.rewards[agent] = (
                        self.game.rounds[-2].points
                        - self.game.rounds[-2].player_points[player]
                    )
            else:
                # there is a round happening so we reward players for avoiding points
                for player in self.game.players:
                    agent = self.player_to_agent_map[player]
                    if self.game.rounds[-1].plays[-1].taker is player:
                        self.rewards[agent] = 0
                    else:
                        self.rewards[agent] = self.game.rounds[-1].plays[-1].points

    def set_next_agent(self):
        next_player = self.game.get_next_player()
        self.agent_selection = self.player_to_agent_map[next_player]


def env():
    environment = raw_env()

    # Recommended wrappers
    # environment = wrappers.OrderEnforcingWrapper(environment)
    # environment = wrappers.AssertOutOfBoundsWrapper(environment)
    # environment = wrappers.CaptureStdoutWrapper(environment)

    return environment


def raw_env():
    return ChujGym()
