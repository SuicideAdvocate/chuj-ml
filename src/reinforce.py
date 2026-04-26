import pettingzoo.test

from chuj_gym import env

environment = env()

pettingzoo.test.api_test(env(), num_cycles=1000)
try:
    print("Environment passes all checks!")
except Exception as e:
    print(f"Environment has issues: {e}")

# # Training hyperparameters
# learning_rate = 0.01  # How fast to learn (higher = faster but less stable)
# n_episodes = 100_000  # Number of hands to practice
# start_epsilon = 1.0  # Start with 100% random actions
# epsilon_decay = start_epsilon / (n_episodes / 2)  # Reduce exploration over time
# final_epsilon = 0.1  # Always keep some exploration
# discount_factor = 0.9
#
# # Create environment and agent
# env = gym.make("Blackjack-v1", sab=False)
# env = gym.wrappers.RecordEpisodeStatistics(env, buffer_length=n_episodes)
#
# agent = ChujAgent(
#     env=env,
#     learning_rate=learning_rate,
#     initial_epsilon=start_epsilon,
#     epsilon_decay=epsilon_decay,
#     final_epsilon=final_epsilon,
#     discount_factor=discount_factor,
# )

# for episode in tqdm(range(n_episodes)):
#     # Start a new hand
#     obs, info = env.reset()
#     done = False
#
#     # Play one complete hand
#     while not done:
#         # Agent chooses action (initially random, gradually more intelligent)
#         action = agent.get_action(obs)
#
#         # Take action and observe result
#         next_obs, reward, terminated, truncated, info = env.step(action)
#
#         if episode % 100 == 0:
#             print(f"Episode {episode}: Reward={reward}")
#
#         # Learn from this experience
#         agent.update(obs, action, reward, terminated, next_obs)
#
#         # Move to next state
#         done = terminated or truncated
#         obs = next_obs
#
#     # Reduce exploration rate (agent becomes less random over time)
#     agent.decay_epsilon()
