from src.ai.q_learning import QLearningAgent

if __name__ == "__main__":
    agent = QLearningAgent()
    print("Training Q-Learning agent...")
    agent.train(episodes=5000)
    agent.save("q_table.pkl")
    print("Training completed and Q-table saved.")
