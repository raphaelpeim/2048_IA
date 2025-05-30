from src.common.constants import DIRECTIONS, MOVE_FUNCTIONS


# Board
def is_same_board(board1, board2):
    return all(
        board1[row][column] == board2[row][column]
        for row in range(len(board1))
        for column in range(len(board1[0]))
    )

def serialize_board(board):
    return tuple(cell for row in board for cell in row)

# Moves
def get_valid_moves(board):
    valid = []
    for direction in DIRECTIONS:
        moved = MOVE_FUNCTIONS[direction]([row[:] for row in board])
        if not is_same_board(moved, board):
            valid.append(direction)
    return valid

def simulate_move(board, move):
    board_copy = [row[:] for row in board]
    return MOVE_FUNCTIONS[move](board_copy)
