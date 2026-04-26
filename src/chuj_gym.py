import pettingzoo

from src import chuj_game


class ChujGym(pettingzoo.AECEnv):
    def __init__(self):
        self.game = chuj_game.Game()

    def reset(self, seed: int | None = None, options: dict | None = None):
        super().reset(seed=seed)

    def step(self, action):
        pass
