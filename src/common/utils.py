import keyboard

from src.common.constants import BOARD_SIZE
from src.common.direction import Direction


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

