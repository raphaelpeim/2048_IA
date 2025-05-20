from src.common.direction import Direction
from src.common.moves import move_up, move_down, move_left, move_right

# Game configuration
BOARD_SIZE = 4

TARGET_TILE = 2048

# Directions and corresponding move functions
DIRECTIONS = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

KEYBOARD_ARROW_DIRECTIONS = {
    'Up': Direction.UP,
    'Down': Direction.DOWN,
    'Left': Direction.LEFT,
    'Right': Direction.RIGHT
}

MOVE_FUNCTIONS = {
    Direction.UP: move_up,
    Direction.DOWN: move_down,
    Direction.LEFT: move_left,
    Direction.RIGHT: move_right
}

# Visualization colors
COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}
