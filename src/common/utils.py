import copy
import keyboard

from src.common.constants import BOARD_SIZE, DIRECTIONS, MOVE_FUNCTIONS
from src.common.direction import Direction
from src.common.moves import move_up, move_down, move_left, move_right


# Board
def print_board(board):
    print("\n" + "-" * (BOARD_SIZE * 6 + 1))
    for row in board:
        row_str = "|".join(f"{num:^5}" if num > 0 else "     " for num in row)
        print(f"|{row_str}|")
        print("-" * (BOARD_SIZE * 6 + 1))

def is_same_board(board1, board2):
    return all(
        board1[row][column] == board2[row][column]
        for row in range(len(board1))
        for column in range(len(board1[0]))
    )

# Keyboard
def get_input():
    print("Use arrow keys to move. Press Esc to quit.")
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'up':
                return Direction.UP
            elif event.name == 'down':
                return Direction.DOWN
            elif event.name == 'left':
                return Direction.LEFT
            elif event.name == 'right':
                return Direction.RIGHT
            elif event.name == 'esc':
                return 'quit'

# Moves
def get_valid_moves(board):
    valid = []
    for direction in DIRECTIONS:
        moved = MOVE_FUNCTIONS[direction](copy.deepcopy(board))
        if not is_same_board(moved, board):
            valid.append(direction)
    return valid

def apply_move(board, move):
        new_board = copy.deepcopy(board)

        if move == Direction.UP:
            new_board = move_up(board)
        elif move == Direction.DOWN:
            new_board = move_down(board)
        elif move == Direction.LEFT:
            new_board = move_left(board)
        elif move == Direction.RIGHT:
            new_board = move_right(board)

        return new_board
