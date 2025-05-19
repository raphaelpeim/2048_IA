import copy
import random

from src.common.constants import DIRECTIONS, MOVE_FUNCTIONS
from src.common.utils import is_same_board


def get_valid_moves(board):
    valid = []
    for direction in DIRECTIONS:
        moved = MOVE_FUNCTIONS[direction](copy.deepcopy(board))
        if not is_same_board(moved, board):
            valid.append(direction)
    return valid

def evaluate(board):
    # Simple heuristic: prefer boards with more empty tiles
    empty = sum(cell == 0 for row in board for cell in row)
    return empty

def get_best_move(board):
    best_score = -1
    best_move = None
    for direction in get_valid_moves(board):
        new_board = MOVE_FUNCTIONS[direction](copy.deepcopy(board))
        score = evaluate(new_board)
        if score > best_score:
            best_score = score
            best_move = direction
    return best_move or random.choice(DIRECTIONS)
