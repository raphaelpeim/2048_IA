import os
import pickle
import random

from src.ai.utils import compute_reward
from src.common.constants import QTABLE_PATH, DIRECTIONS
from src.common.utils import serialize_board, is_same_board, simulate_move
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
        # Get table value for state and move combination or 0
        return self.q_table.get((state, move), 0.0)

    def update_q(self, state, move, reward, next_state, next_valid_moves):
        # Looking for maximum known value for all valid moves
        max_q = max([self.get_q(next_state, a) for a in next_valid_moves], default=0)
        # Get (state, move) corresponding value
        current_q = self.get_q(state, move)
        # Q[state, move] = Q[state, move] + α * (reward + γ * max(Q[next_state, a]) - Q[state, move])
        #
        # Q[state, move]      : Current estimated value for taking move in state.
        # α (alpha)             : Learning rate (how much new info overrides old).
        # reward                : Immediate reward received after taking the move.
        # γ (gamma)             : Discount factor (importance of future rewards).
        # max(Q[next_state, a]) : Best possible future reward from next_state.
        self.q_table[(state, move)] = current_q + self.alpha * (reward + self.gamma * max_q - current_q)

    def get_move(self, state, valid_moves):
        # Random choice to explore or not
        if random.random() < self.epsilon:
            return random.choice(valid_moves)
        # Choose the best action
        qs = {action: self.get_q(state, action) for action in valid_moves}
        return max(qs, key=qs.get)

    def decay_epsilon(self):
        # Reduce epsilon, form exploration to exploitation until min_epsilon
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
            new_board = simulate_move(old_board, move)

            if is_same_board(old_board, new_board):
                continue  # Skip invalid move

            reward = compute_reward(old_board, new_board)
            total_score += reward
            game.board = new_board
            game.add_tile()

            new_state = serialize_board(game.board)
            self.update_q(state, move, reward, new_state, next_valid_moves=[move])

            if game.is_won():
                return (total_score, max(max(row) for row in game.board), True) if return_max_tile else total_score

            if not game.can_move():
                return (total_score, max(max(row) for row in game.board), False) if return_max_tile else total_score
