import numpy as np
import random

from src.common.constants import BOARD_SIZE, TARGET_TILE


class Game2048:
    def __init__(self):
        # Create a nxn grid filled with zeros (empty)
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        # Add two tiles to start
        self.add_tile()
        self.add_tile()

    def add_tile(self):
        empty = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.board[i][j] == 0]

        if empty:
            i, j = random.choice(empty)  # Uses Python’s stdlib random
            self.board[i][j] = random.choices([2, 4], weights=[0.9, 0.1])[0]  # Optional: bias toward 2

    def is_won(self):
        return any(cell == TARGET_TILE for row in self.board for cell in row)

    def can_move(self):
        board = self.board

        # 1. Empty cell exists
        for row in board:
            if 0 in row:
                return True

        # 2. Mergeable horizontal neighbors
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE - 1):
                if board[i][j] == board[i][j + 1]:
                    return True

        # 3. Mergeable vertical neighbors
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE - 1):
                if board[i][j] == board[i + 1][j]:
                    return True

        return False

