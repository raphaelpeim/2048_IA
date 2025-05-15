import numpy as np
import random

class Game2048:
    def __init__(self):
        # Create a 4x4 grid filled with zeros (empty)
        self.board = np.zeros((4, 4), dtype=int)
        # Add two tiles to start
        self.add_tile()
        self.add_tile()

    def add_tile(self):
        # Find empty positions (zeros)
        empty = list(zip(*np.where(self.board == 0)))

        if empty:
            # Pick a random empty position
            i, j = random.choice(empty)
            # Add a 2 (90%) or 4 (10%)
            self.board[i][j] = 2 if random.random() < 0.9 else 4