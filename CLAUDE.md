# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

The `.env` file sets `PYTHONPATH=src`, which must be active for imports to resolve. Load it before running any command:

```bash
# Run all tests
set -a && source .env && set +a && python -m unittest discover -v -s tests -p "test_*.py"

# Run a single test file
set -a && source .env && set +a && python -m unittest tests/game/test_chuj_play.py -v

# Run a single test case
set -a && source .env && set +a && python -m unittest tests.game.test_chuj_play.TestChujPlay.test_initial_state_is_not_done -v

# Run reinforce.py (PettingZoo api_test)
set -a && source .env && set +a && python src/reinforce.py
```

Tests use the standard `unittest` module (not pytest). Formatter is `black`.

## Architecture

The project trains RL agents to play **Chuj** — a Polish trick-taking card game. It is split into two layers:

### Game engine (`src/game/`)

Pure game logic with no ML dependencies.

- `ChujConstants` — shared constants: 4 players, 32-card deck, 8-card hands, 175 max points.
- `ChujCard` — a single card with suite, value, index (1-based position in deck), and computed points. Hearts = 1 pt each; Acorns UBER = 4 pts; Leaves UBER = 8 pts; everything else = 0.
- `ChujDeck` — builds all 32 cards (4 suites × 8 values via `itertools.product`) and deals shuffled hands.
- `ChujHand` — a player's current cards; exposes padded numpy vectors for the observation space.
- `ChujPlayer` — holds a `ChujHand` and accumulated `points`.
- `ChujPlay` — one trick (up to 4 cards). Determines the taker: first card leads, higher card of the same suite wins. Exposes a padded card-index vector.
- `ChujRound` — one full deal of 8 tricks. Tracks `player_points` and `player_cards` per taker. Special rule: if only one player takes tricks in a round, they score 0 and all others score `round.points` (20).
- `ChujGame` — orchestrates multiple rounds until any player exceeds 100 points (game ends at end of that round). Re-deals hands from the same `ChujDeck` instance after each round.

**Turn order** is managed by `ChujGame.get_next_player()`:
- First play of a new round → player at index `len(rounds) % 4`.
- First card of a new trick → winner (taker) of the previous trick.
- Mid-trick → next player clockwise from the last who played.

### RL environment (`src/`)

- `ChujGym` — a [PettingZoo](https://pettingzoo.farama.org/) `AECEnv` wrapping `ChujGame`. Agents are named `agent_0`…`agent_3`. Action space is `Discrete(32, start=1)` matching card indexes. Observation is currently minimal (`player_score` only — fuller observations are stubbed out in comments). Action masks (`info["action_mask"]`) reflect the player's current hand.
- `ChujAgent` — Q-learning agent stub (fully commented out, not yet implemented).
- `reinforce.py` — entry point that runs `pettingzoo.test.api_test` to validate the environment.
- `playground.py` — scratch file for ad-hoc experiments.

### Key invariant

`ChujDeck` is a single shared instance per game. Cards are objects with identity — the same `ChujCard` instance is referenced by the deck, hand, play, and round simultaneously. Identity checks (`is`) are used throughout to guard against duplicate plays.
