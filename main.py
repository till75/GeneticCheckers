# main.py
import time
from genetic import GeneticAlgorithm
from agent import MinimaxAgent
from tournament import Match
import matplotlib.pyplot as plt


def plot_training_run(history):
    gens = history["generation"]

    # Create a figure with 2 subplots (Fitness on top, Weights on bottom)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # --- Plot 1: Fitness Progression ---
    ax1.plot(gens, history["best_fitness"], label="Best Fitness", color="forestgreen", marker="o", linewidth=2)
    ax1.plot(gens, history["avg_fitness"], label="Population Avg Fitness", color="gray", linestyle="--", marker="x")
    ax1.set_ylabel("Fitness Score")
    ax1.set_title("Checkers GA: Fitness Evolution Over Generations")
    ax1.legend()
    ax1.grid(True, linestyle=":", alpha=0.6)

    # --- Plot 2: Weight Trajectories ---
    weights_transposed = list(zip(*history["best_weights"]))
    weight_labels = ["Regular Piece", "King Piece", "Center Control", "Back-Row Defense"]
    colors = ["royalblue", "darkorange", "purple", "crimson"]

    for weights, label, color in zip(weights_transposed, weight_labels, colors):
        ax2.plot(gens, weights, label=label, color=color, marker="s", linewidth=2)

    ax2.set_xlabel("Generation")
    ax2.set_ylabel("Weight Value")
    ax2.set_title("Evolution of Heuristic Weights (Best Agent per Generation)")
    ax2.legend(loc="upper left")
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    plt.savefig("checkers_evolution_plot.png", dpi=300)
    print("Saved training plot as 'checkers_evolution_plot.png'")
    plt.show()


def showcase():
    print("=== CHECKERS: Champion vs. Baseline Showcase ===")

    # 1. Define the Gen 1 Baseline Agent (using typical random-ish weights from your initial pool)
    baseline_agent = MinimaxAgent(
        name="Gen1_Baseline",
        weights=[10.0, 20.0, 2.0, 1.0],
        depth=3
    )

    # 2. Define your Evolved Gen 5 Elite Champion
    # (Using the winning weights that emerged and stabilized in your run)
    champion_agent = MinimaxAgent(
        name="Gen5_Elite_Champion",
        weights=[15.16, 18.34, 4.72, 3.02],
        depth=3
    )

    print(f"\nMatchup:")
    print(f"Red (Player 1): {baseline_agent} (Weights: {baseline_agent.weights})")
    print(f"Blue (Player 2): {champion_agent} (Weights: {champion_agent.weights})")
    print("\nStarting visual match in 3 seconds...")
    time.sleep(3)

    # 3. Run a single match with verbose=True so you can watch it play out step-by-step
    # In Game 1: Baseline is Red, Champion is Blue
    match = Match(baseline_agent, champion_agent, max_moves=150, verbose=True)
    red_fit, blue_fit = match.run()

    print("\n=== SHOWCASE MATCH RESULTS ===")
    print(f"{baseline_agent} (Red) Fitness Score: {red_fit:.1f}")
    print(f"{champion_agent} (Blue) Fitness Score: {blue_fit:.1f}")

    if blue_fit > red_fit:
        print(f"\nVictory for the Evolved Champion ({champion_agent})!")
    else:
        print(f"\nBaseline agent pulled an upset!")

def genetic_training():
    # Initialize GA (e.g., 8 agents, depth 3, 20% mutation chance)
    ga = GeneticAlgorithm(
        population_size=20,
        depth=3,
        mutation_rate=0.35,
        mutation_strength=2.5,
        elite_count=2
    )

    num_generations = 25
    for gen in range(num_generations):
        start_time = time.time()
        ga.evolve_generation()
        elapsed = time.time() - start_time
        print(f"Generation completed in {elapsed:.2f} seconds.")

    print("\n=== Training Complete! ===")

    plot_training_run(ga.history)


def main():
    print("=== CHECKERS: Evolutionary Training ===")

    genetic_training()



if __name__ == "__main__":
    main()