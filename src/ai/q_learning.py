import pickle
import random
from src.common.constants import MOVE_FUNCTIONS
from src.common.utils import get_valid_moves
from src.core.game import Game2048


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_state(self, board):
        return tuple(tuple(row) for row in board)

    def choose_action(self, state, valid_actions):
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        q_vals = [self.q_table.get((state, a), 0) for a in valid_actions]
        max_q = max(q_vals)
        return random.choice([a for a, q in zip(valid_actions, q_vals) if q == max_q])

    def learn(self, s, a, r, s_next, valid_actions_next):
        old_q = self.q_table.get((s, a), 0)
        future_q = max([self.q_table.get((s_next, a2), 0) for a2 in valid_actions_next], default=0)
        new_q = old_q + self.alpha * (r + self.gamma * future_q - old_q)
        self.q_table[(s, a)] = new_q

    def train(self, episodes=10000):
        for episode in range(episodes):
            game = Game2048()
            while game.can_move():
                s = self.get_state(game.board)
                valid = get_valid_moves(game.board)
                a = self.choose_action(s, valid)
                new_board = MOVE_FUNCTIONS[a](game.board)
                reward = self.calculate_reward(game.board, new_board)
                game.board = new_board
                game.add_tile()
                s_next = self.get_state(game.board)
                valid_next = get_valid_moves(game.board)
                self.learn(s, a, reward, s_next, valid_next)

    def calculate_reward(self, old_board, new_board):
        return sum(sum(new_row) for new_row in new_board) - sum(sum(row) for row in old_board)

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load(self, path):
        with open(path, 'rb') as f:
            self.q_table = pickle.load(f)
