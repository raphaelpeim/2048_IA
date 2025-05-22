import os
import pickle
import random

from src.common.constants import QTABLE_PATH, DIRECTIONS, MOVE_FUNCTIONS
from src.common.utils import serialize_board, is_same_board, compute_reward
from src.core.game import Game2048


class QLearningAgent:
    def __init__(self, alpha=0.5, gamma=0.95, epsilon=1.0, decay=0.999, min_epsilon=0.05):
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

    def get_q(self, state, move):
        # Get table value for state and move combined or 0 if unknown
        return self.q_table.get((state, move), 0.0)

    def update(self, state, move, reward, next_state, next_valid_moves):
        # Looking for maximum known value for all valid moves
        max_q = max([self.get_q(next_state, a) for a in next_valid_moves], default=0)
        # Get (state, move) corresponding value
        current_q = self.get_q(state, move)
        # Q[state, action] = Q[state, action] + α * (reward + γ * max(Q[next_state, a]) - Q[state, action])
        #
        # Q[state, action]      : Current estimated value for taking action in state.
        # α (alpha)             : Learning rate (how much new info overrides old).
        # reward                : Immediate reward received after taking the action.
        # γ (gamma)             : Discount factor (importance of future rewards).
        # max(Q[next_state, a]) : Best possible future reward from next_state.
        self.q_table[(state, move)] = current_q + self.alpha * (reward + self.gamma * max_q - current_q)

    def get_action(self, state, valid_actions):
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        qs = {a: self.get_q(state, a) for a in valid_actions}
        return max(qs, key=qs.get)

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay)

    def play_game(self, return_max_tile=False):
        game = Game2048()
        total_score = 0

        while True:
            state = serialize_board(game.board)
            if random.random() < self.epsilon:
                move = random.choice(DIRECTIONS)
            else:
                move = self.get_q(self.q_table, state)

            old_board = [row[:] for row in game.board]
            new_board = MOVE_FUNCTIONS[move](old_board)

            if is_same_board(old_board, new_board):
                continue  # Skip invalid move

            reward = compute_reward(old_board, new_board)
            total_score += reward
            game.board = new_board
            game.add_tile()

            new_state = serialize_board(game.board)
            self.update(state, move, reward, new_state, next_valid_moves=[move])

            if game.is_won():
                return (total_score, max(max(row) for row in game.board), True) if return_max_tile else total_score

            if not game.can_move():
                return (total_score, max(max(row) for row in game.board), False) if return_max_tile else total_score
