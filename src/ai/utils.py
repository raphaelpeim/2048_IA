import csv
import pickle

from matplotlib import pyplot as plt
from src.common.constants import QTABLE_PATH, DIRECTIONS, MOVE_FUNCTIONS
from src.common.utils import serialize_board, get_valid_moves, simulate_move, is_same_board
from src.core.game import Game2048


EPISODES = 10000
SAVE_EVERY = 500

# Train
def compute_reward(old_board, new_board, won=False, game_over=False):
    # The new board have to be different from the old one
    if is_same_board(old_board, new_board):
        return -5

    # Merging tiles is encourage, especially high values
    score_gain = sum(
        max(new_tile - old_tile, 0)
        for new_row, old_row in zip(new_board, old_board)
        for new_tile, old_tile in zip(new_row, old_row)
    )
    # The more there is zero cell, the better it is
    empty_tiles = sum(cell == 0 for row in new_board for cell in row)
    # Bonus according to next state
    bonus = 100 if won else -50 if game_over else 0
    return score_gain + empty_tiles * 0.5 + bonus

def train(agent, episodes=1000, log = False):
    scores = []
    max_tiles = []

    for episode in range(episodes):
        game = Game2048()
        state = serialize_board(game.board)
        total_score = 0

        while game.can_move():
            # Action
            valid_moves = get_valid_moves(game.board)
            move = agent.get_move(state, valid_moves)
            new_board = simulate_move(game.board, move)
            # Reward
            reward = compute_reward(game.board, new_board)
            # Update qtable
            next_state = serialize_board(new_board)
            next_moves = get_valid_moves(new_board)
            agent.update_q(state, move, reward, next_state, next_moves)
            # Save
            game.board = new_board
            state = next_state
            total_score += reward
            # New tile
            game.add_tile()

        scores.append(total_score)
        max_tiles.append(max(cell for row in game.board for cell in row))
        agent.decay_epsilon()

        if log and episode % 100 == 0:
            print(f"Episode {episode} - Score: {total_score}, Max tile: {max_tiles[-1]}, Epsilon: {agent.epsilon:.4f}")

    # Save Q-table
    with open(QTABLE_PATH, "wb") as file:
        pickle.dump(agent.q_table, file)

    visualize_training(scores, max_tiles)

def train_with_savings(agent, episodes=EPISODES):
    scores = []
    wins = 0

    for episode in range(1, episodes + 1):
        game = Game2048()
        total_reward = 0
        steps = 0

        while game.can_move():
            state = serialize_board(game.board)
            valid_moves = [d for d in DIRECTIONS if not is_same_board(game.board, MOVE_FUNCTIONS[d](game.board))]

            action = agent.get_move(state, valid_moves)
            new_board = MOVE_FUNCTIONS[action](game.board)
            reward = compute_reward(game.board, new_board, won=game.is_won(), game_over=not game.can_move())

            new_state = serialize_board(new_board)
            agent.update_q(state, action, reward, new_state, new_board)

            if not is_same_board(game.board, new_board):
                game.board = new_board
                game.add_tile()

            total_reward += reward
            steps += 1

            if game.is_won():
                wins += 1
                break

        agent.decay_epsilon()
        scores.append(total_reward)

        # Logging
        if episode % 100 == 0:
            print(f"Episode {episode}: Score={int(total_reward)}, Steps={steps}, Wins={wins}")

        if episode % SAVE_EVERY == 0:
            with open(QTABLE_PATH, "wb") as f:
                pickle.dump(agent.q_table, f)
            print(f"Saved Q-table at episode {episode}")

    with open("assets/training_scores.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Episode", "Score"])
        for i, s in enumerate(scores, 1):
            writer.writerow([i, s])

    return scores, wins

# Visualize
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

def read_scores(csv_path):
    episodes = []
    scores = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            episodes.append(int(row["Episode"]))
            scores.append(float(row["Score"]))
    return episodes, scores

def smooth(data, window_size=100):
    return [sum(data[i:i + window_size]) / window_size for i in range(len(data) - window_size + 1)]

def plot_scores(csv_path):
    episodes, scores = read_scores(csv_path)

    plt.figure(figsize=(12, 6))
    plt.plot(episodes, scores, label="Raw Score", alpha=0.4)

    if len(scores) >= 100:
        smoothed = smooth(scores, window_size=100)
        plt.plot(episodes[:len(smoothed)], smoothed, label="Smoothed (window=100)", color='orange')

    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.title("Q-Learning Training Scores Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
