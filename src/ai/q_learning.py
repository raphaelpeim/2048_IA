import os
import pickle
import random

from src.common.constants import QTABLE_PATH


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, decay=0.995, min_epsilon=0.01):
        # Learning rate
        self.alpha = alpha
        # Discount future rewards
        self.gamma = gamma
        # Exploration rate
        self.epsilon = epsilon
        # How quickly `epsilon` shrinks
        self.decay = decay
        # Minimum exploration
        self.min_epsilon = min_epsilon
        # Try loading qtable
        if os.path.exists(QTABLE_PATH):
            with open(QTABLE_PATH, "rb") as file:
                self.q_table = pickle.load(file)
        else:
            self.q_table = {}

    def get_q(self, state, action):
        # Get table value for state and action combined or 0 if unknown
        return self.q_table.get((state, action), 0.0)

    def update(self, state, action, reward, next_state, next_valid_actions):
        # Looking for maximum known value with all valid actions
        max_q = max([self.get_q(next_state, a) for a in next_valid_actions], default=0)
        # Get (state, action) corresponding value
        current_q = self.get_q(state, action)
        # Q[state, action] = Q[state, action] + α * (reward + γ * max(Q[next_state, a]) - Q[state, action])
        #
        # Q[state, action]      : Current estimated value for taking action in state.
        # α (alpha)             : Learning rate (how much new info overrides old).
        # reward                : Immediate reward received after taking the action.
        # γ (gamma)             : Discount factor (importance of future rewards).
        # max(Q[next_state, a]) : Best possible future reward from next_state.
        self.q_table[(state, action)] = current_q + self.alpha * (reward + self.gamma * max_q - current_q)

    def get_action(self, state, valid_actions):
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        qs = {a: self.get_q(state, a) for a in valid_actions}
        return max(qs, key=qs.get)

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay)
