import itertools
from statistics import mean

from src.ai.q_learning import QLearningAgent

# Parameter grid
alphas = [0.1, 0.3, 0.5]
gammas = [0.9, 0.95, 0.99]
epsilons = [1.0]
decays = [0.995, 0.999]
min_epsilons = [0.05]

parameter_combinations = list(itertools.product(alphas, gammas, epsilons, decays, min_epsilons))

def run_benchmark(games_per_combo=30):
    results = []

    for i, (alpha, gamma, epsilon, decay, min_eps) in enumerate(parameter_combinations, 1):
        print(f"[{i}/{len(parameter_combinations)}] Testing α={alpha}, γ={gamma}, ε={epsilon}, decay={decay}, min_ε={min_eps}")

        agent = QLearningAgent(
            alpha=alpha,
            gamma=gamma,
            epsilon=epsilon,
            decay=decay,
            min_epsilon=min_eps
        )

        scores = []
        max_tiles = []
        wins = 0

        for _ in range(games_per_combo):
            score, max_tile, won = agent.play_game(return_max_tile=True)
            scores.append(score)
            max_tiles.append(max_tile)
            if won:
                wins += 1

        avg_score = mean(scores)
        avg_tile = mean(max_tiles)
        win_rate = wins / games_per_combo

        results.append({
            "params": (alpha, gamma, epsilon, decay, min_eps),
            "avg_score": avg_score,
            "avg_max_tile": avg_tile,
            "win_rate": win_rate
        })

    # Sort by average score
    results.sort(key=lambda r: r["avg_score"], reverse=True)

    print("\n🏆 Top 5 Configurations:")
    for result in results[:5]:
        p = result["params"]
        print(f"α={p[0]}, γ={p[1]}, ε={p[2]}, decay={p[3]}, min_ε={p[4]} | "
              f"Score: {result['avg_score']:.1f}, Max Tile: {result['avg_max_tile']:.0f}, Win Rate: {result['win_rate']:.2%}")

if __name__ == "__main__":
    run_benchmark()
