import keyboard
import matplotlib.pyplot as plt

from src.common.constants import BOARD_SIZE, DIRECTIONS, MOVE_FUNCTIONS
from src.common.direction import Direction
from src.common.moves import move_up, move_down, move_left, move_right
from src.core.game import Game2048


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

def serialize_board(board):
    return tuple(cell for row in board for cell in row)

def compute_reward(old_board, new_board):
    score_gain = sum(sum(new - old for new, old in zip(nr, orow) if new > old) for nr, orow in zip(new_board, old_board))
    empty_tiles = sum(cell == 0 for row in new_board for cell in row)
    return score_gain + empty_tiles * 0.1

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
        moved = MOVE_FUNCTIONS[direction]([row[:] for row in board])
        if not is_same_board(moved, board):
            valid.append(direction)
    return valid

def simulate_move(board, move):
    board_copy = [row[:] for row in board]
    return MOVE_FUNCTIONS[move](board_copy)

# Visualization
def visualize_training(scores, max_tiles):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(scores, label='Score')
    plt.title('Episode Scores')
    plt.xlabel('Episode')
    plt.ylabel('Score')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(max_tiles, label='Max Tile', color='orange')
    plt.title('Max Tile per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Tile Value')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# AI
def train(agent, episodes=1000):
    # TODO analyze

    scores = []
    max_tiles = []

    for episode in range(episodes):
        game = Game2048()
        state = serialize_board(game.board)
        total_score = 0

        while game.can_move():
            valid_moves = get_valid_moves(game.board)
            action = agent.get_action(state, valid_moves)

            new_board = simulate_move(game.board, action)
            reward = compute_reward(game.board, new_board)
            total_score += reward

            next_state = serialize_board(new_board)
            next_moves = get_valid_moves(new_board)

            agent.update(state, action, reward, next_state, next_moves)
            game.board = new_board
            state = next_state

            print_board(game.board)

        scores.append(total_score)
        max_tiles.append(max(cell for row in game.board for cell in row))
        agent.decay_epsilon()

        if episode % 100 == 0:
            print(f"Episode {episode} - Score: {total_score}, Max tile: {max_tiles[-1]}, Epsilon: {agent.epsilon:.4f}")

    visualize_training(scores, max_tiles)
