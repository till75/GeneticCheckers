# genetic.py
import random
from agent import MinimaxAgent
from tournament import TournamentManager


class GeneticAlgorithm:
    """Manages population evolution, selection, crossover, and mutation."""

    def __init__(self, population_size=10, depth=3, mutation_rate=0.2, mutation_strength=2.0, elite_count=2):
        self.population_size = population_size
        self.depth = depth
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.elite_count = elite_count

        # Initialize tournament manager which holds the population
        self.tournament_manager = TournamentManager(population_size=population_size, depth=depth)
        self.generation = 1
        self.history = {
            "generation": [],
            "best_fitness": [],
            "avg_fitness": [],
            "best_weights": [],
            "draw_pct": [],
            "avg_winner_moves": []
        }

    def evolve_generation(self):
        """Runs one full generation: tournament evaluation -> selection -> crossover -> mutation."""
        print(f"\n--- Starting Generation {self.generation} ---")

        # 1. Evaluate current population via tournament round-robin
        ranked_population, match_stats = self.tournament_manager.run_round_robin()

        # Print top performer of the generation
        top_agent, top_fitness = ranked_population[0]
        decisive_pct = 100.0 - match_stats["draw_pct"]
        print(
            f"   [Diagnostics] Matches: {match_stats['total_matches']} | Decisive / Advantage: {decisive_pct:.1f}% | "
            f"Stagnant Draws: {match_stats['draw_pct']:.1f}% | Avg Winner Moves: {match_stats['avg_winner_moves']:.1f}")
        print(
            f"Gen {self.generation} Best -> {top_agent} (Fitness: {top_fitness:.1f}) | Weights: {[round(w, 2) for w in top_agent.weights]}")

        avg_fitness = sum(fit for _, fit in ranked_population) / len(ranked_population)

        # Record history for plotting
        self.history["generation"].append(self.generation)
        self.history["best_fitness"].append(top_fitness)
        self.history["avg_fitness"].append(avg_fitness)
        self.history["best_weights"].append(list(top_agent.weights))
        self.history["draw_pct"].append(match_stats["draw_pct"])
        self.history["avg_winner_moves"].append(match_stats["avg_winner_moves"])

        # Extract just the agent objects in order of fitness (best to worst)
        sorted_agents = [agent for agent, fitness in ranked_population]

        # 2. Elitism: Carry over the top N agents unchanged
        new_population = []
        for i in range(self.elite_count):
            elite_parent = sorted_agents[i]
            # Create a clean clone/copy with a refreshed generation name
            elite_clone = MinimaxAgent(
                name=f"Gen{self.generation + 1}_Elite_{i + 1}",
                weights=list(elite_parent.weights),
                depth=self.depth
            )
            new_population.append(elite_clone)

        # 3. Breed the rest of the population
        agent_counter = self.elite_count + 1
        while len(new_population) < self.population_size:
            # Select parents using tournament selection
            parent_a = self._select_parent(ranked_population)
            parent_b = self._select_parent(ranked_population)

            # Crossover: Blend weights
            child_weights = self._crossover(parent_a.weights, parent_b.weights)

            # Mutation: Perturb weights randomly
            child_weights = self._mutate(child_weights)

            child_agent = MinimaxAgent(
                name=f"Gen{self.generation + 1}_Agent_{agent_counter}",
                weights=child_weights,
                depth=self.depth
            )
            new_population.append(child_agent)
            agent_counter += 1

        # Update tournament manager's population for the next generation
        self.tournament_manager.population = new_population
        self.generation += 1
        return top_agent, top_fitness

    def _select_parent(self, ranked_population):
        """Selects a parent using tournament selection (picks the best of 3 random candidates)."""
        pool_size = min(4, len(ranked_population))
        candidates = random.sample(ranked_population, pool_size)
        # candidates contains tuples of (agent, fitness)
        candidates.sort(key=lambda item: item[1], reverse=True)
        return candidates[0][0]  # Return the agent object with highest fitness in sample

    def _crossover(self, weights_a, weights_b):
        """Performs uniform crossover between two weight vectors."""
        child_weights = []
        for w_a, w_b in zip(weights_a, weights_b):
            # 50% chance to take from parent A or parent B
            chosen_weight = w_a if random.random() < 0.5 else w_b
            child_weights.append(chosen_weight)
        return child_weights

    def _mutate(self, weights):
        """Applies Gaussian mutation to weights based on mutation rate and strength."""
        mutated_weights = []
        for w in weights:
            if random.random() < self.mutation_rate:
                # Add random Gaussian noise
                noise = random.gauss(0, self.mutation_strength)
                new_w = max(0.1, w + noise)  # Keep weights positive
                mutated_weights.append(new_w)
            else:
                mutated_weights.append(w)
        return mutated_weights