from src.ai.q_learning import QLearningAgent
from src.common.utils import train

if __name__ == "__main__":
    agent = QLearningAgent()
    train(agent, episodes=10000)
