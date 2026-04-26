from typing import Dict

import gymnasium
import numpy
import pettingzoo

from src.game.chuj_deck import ChujDeck
from src.game.chuj_game import ChujGame
from src.game.chuj_hand import ChujHand
from src.game.chuj_play import ChujPlay
from src.game.chuj_player import ChujPlayer


class ChujGym(pettingzoo.AECEnv):
    loss_points = -1000

    def __init__(self):
        super().__init__()

        self.possible_agents = ["agent_0", "agent_1", "agent_2", "agent_3"]
        self.agents = self.possible_agents.copy()

        self.action_spaces = {
            agent: gymnasium.spaces.Discrete(32, start=1) for agent in self.agents
        }

        self.observation_spaces = {
            agent: gymnasium.spaces.Dict(
                {
                    "player_score": gymnasium.spaces.Discrete(ChujGame.max_points + 1),
                    "opponent_scores": gymnasium.spaces.MultiDiscrete(
                        [ChujGame.max_points + 1] * (ChujPlay.size - 1)
                    ),
                    "current_round_played_cards": gymnasium.spaces.MultiDiscrete(
                        [ChujDeck.size + 1] * ChujDeck.size),
                    "current_play_played_cards": gymnasium.spaces.MultiDiscrete(
                        [ChujDeck.size + 1] * ChujPlay.size),
                    "curent_round_taken_cards": gymnasium.spaces.MultiDiscrete(
                        [ChujDeck.size + 1] * ChujPlay.size),
                    "current_hand": gymnasium.spaces.MultiDiscrete(
                        [ChujDeck.size + 1] * ChujHand.size),
                }
            ) for agent in self.agents
        }

        self.game: ChujGame = ChujGame()
        self.agents_map: Dict[str, ChujPlayer] = self.map_agents_to_players()
        self.players_map: Dict[ChujPlayer, str] = self.map_players_to_agents()
        self.iteration = 0

    def reset(self, seed: int | None = None, options: dict | None = None):
        numpy.random.seed(seed)

        self.agents = self.possible_agents.copy()
        self.agent_selection = self.agents[0]

        self.game = ChujGame()
        self.agents_map = self.map_agents_to_players()
        self.players_map = self.map_players_to_agents()

        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}

    def observe(self, agent):
        player = self.agents_map[agent]
        return {
            "player_score": player.points,
            "opponent_scores": self.game.get_opponent_scores_vector(player),
            "current_round_played_cards": self.game.rounds[-1].get_played_cards_padded_vector(),
            "current_play_played_cards": self.game.rounds[-1].plays[-1].get_played_cards_padded_vector(),
            "curent_round_taken_cards": self.game.rounds[-1].get_taken_cards_padded_vector(player),
            "current_hand": player.hand.get_cards_padded_vector(),
        }

    def step(self, action):
        # increment the iteration to keep track of the current step in the game
        self.iteration += 1

        # select the next player
        next_player = self.game.get_next_player()

        # play a card based on the next player decision to move the environment
        card_to_play = [card for card in self.game.deck.cards][0]
        self.game.play_card(card_to_play, next_player)

        # if there are 4 iterations, it means all agents have had a turn and we can distribute rewards
        if self.iteration == 4:
            # reset the iteration for the next round of steps
            self.iteration = 0

            # assign rewards to the players
            if self.game.is_done:
                # if the game is done, assign rewards based on the final scores
                # losers get negative rewards, while the survivors get reward based on how far from 100 points they are
                for player in self.game.players:
                    agent = self.players_map[player]
                    self.rewards[agent] = ChujGym.loss_points \
                        if player.points > 100 \
                        else 100 - player.points
            elif self.game.rounds[-1].is_empty:
                # if the latest round is empty, we one round before that has just been completed
                # we reward players with points, they have avoided
                for player in self.game.players:
                    agent = self.players_map[player]
                    self.rewards[agent] = self.game.rounds[-2].points - self.game.rounds[-2].player_points[player]
            else:
                # there is a round happening so we reward players for avoiding points
                for player in self.game.players:
                    agent = self.players_map[player]
                    if self.game.rounds[-1].plays[-1].taker is player:
                        self.rewards[agent] = 0
                    else:
                        self.rewards[agent] = self.game.rounds[-1].plays[-1].points

    def map_agents_to_players(self):
        return {agent: self.game.players[i] for i, agent in enumerate(self.agents)}

    def map_players_to_agents(self):
        return {player: agent for agent, player in self.agents_map.items()}


def env():
    environment = raw_env()

    # Recommended wrappers
    # environment = wrappers.OrderEnforcingWrapper(environment)
    # environment = wrappers.AssertOutOfBoundsWrapper(environment)
    # environment = wrappers.CaptureStdoutWrapper(environment)

    return environment


def raw_env():
    return ChujGym()
