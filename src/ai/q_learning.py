import random
import pickle

from src.common.utils import is_same_board
from src.common.constants import DIRECTIONS, MOVE_FUNCTIONS
from src.core.game import Game2048
import matplotlib.pyplot as plt

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, decay=0.995, min_epsilon=0.01):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.decay = decay
        self.min_epsilon = min_epsilon

    def get_q(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def update(self, state, action, reward, next_state, next_valid_actions):
        max_q = max([self.get_q(next_state, a) for a in next_valid_actions], default=0)
        current_q = self.get_q(state, action)
        self.q_table[(state, action)] = current_q + self.alpha * (reward + self.gamma * max_q - current_q)

    def get_action(self, state, valid_actions):
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        qs = {a: self.get_q(state, a) for a in valid_actions}
        return max(qs, key=qs.get)

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay)
