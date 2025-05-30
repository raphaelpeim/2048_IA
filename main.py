from src.ai.q_learning import QLearningAgent
from src.ai.utils import train, train_with_savings

if __name__ == "__main__":
    agent = QLearningAgent()
    train_with_savings(agent, episodes=10000)
