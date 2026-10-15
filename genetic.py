import random
from agent import MinimaxAgent
from tournament import TournamentManager
from hall_of_fame import HallOfFame
from tournament import Match


class GeneticAlgorithm:
    """Manages population evolution, selection, crossover, and mutation."""

    def __init__(self, population_size=10, depth=3, mutation_rate=0.2, mutation_strength=2.0, elite_count=2):
        self.population_size = population_size
        self.depth = depth
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.elite_count = elite_count

        # Initialize tournament manager and Hall of Fame
        self.tournament_manager = TournamentManager(population_size=population_size, depth=depth)
        self.hof = HallOfFame(max_size=5)
        self.hof.load_from_disk()  # Restores your pre-seeded historical champions

        self.generation = 1
        self.history = {
            "generation": [],
            "best_fitness": [],
            "avg_fitness": [],
            "best_weights": [],
            "draw_pct": [],
            "avg_winner_moves": [],
            "hof_benchmark_score": []  # Tracks absolute performance percentage
        }

    def evolve_generation(self):
        """Runs one full generation: tournament evaluation -> HoF benchmark -> selection -> crossover -> mutation."""
        print(f"\n--- Starting Generation {self.generation} ---")

        # 1. Evaluate current population via tournament round-robin
        ranked_population, match_stats = self.tournament_manager.run_round_robin()
        top_agent, top_fitness = ranked_population[0]

        # 2. Absolute Benchmark: Test population against existing historical Titans (Symmetric 2-game series)
        hof_percentage = 0.0
        hof_agents = self.hof.get_benchmark_agents(self.depth)
        if len(hof_agents) > 0:
            total_score_sum = 0
            total_possible_points = 0
            sample_agents = [agent for agent, _ in ranked_population[:5]]  # test top 5

            for cur_agent in sample_agents:
                for hof_champ in hof_agents:
                    if cur_agent.name == hof_champ.name:
                        continue

                    # Game 1: cur_agent (Red) vs hof_champ (Blue)
                    match_1 = Match(cur_agent, hof_champ, verbose=False)
                    fit_cur1, fit_hof1, outcome_1 = match_1.run()
                    total_possible_points += 3

                    if fit_cur1 > fit_hof1:
                        total_score_sum += 3
                    elif "Draw" in outcome_1 or "Stalemate" in outcome_1:
                        total_score_sum += 1

                    # Game 2: hof_champ (Red) vs cur_agent (Blue) [Swapped sides]
                    match_2 = Match(hof_champ, cur_agent, verbose=False)
                    fit_hof2, fit_cur2, outcome_2 = match_2.run()
                    total_possible_points += 3

                    if fit_cur2 > fit_hof2:
                        total_score_sum += 3
                    elif "Draw" in outcome_2 or "Stalemate" in outcome_2:
                        total_score_sum += 1

            hof_score = total_score_sum / max(1, total_possible_points)
            hof_percentage = hof_score * 100.0
            print(f"   [HoF Benchmark] Average Performance vs Historical Titans: {hof_percentage:.1f}%")

        # 3. Update Hall of Fame with the generation's champion (using gated logic)
        # Pass the calculated benchmark percentage into the gate
        self.hof.add_champion(self.generation, top_agent, benchmark_percentage=hof_percentage)
        self.hof.save_to_disk()

        # Define readable labels for your 6 weights
        weight_labels = ["Reg", "King", "Center", "BackRow", "Edge", "Endgame"]
        formatted_weights = {label: round(w, 2) for label, w in zip(weight_labels, top_agent.weights)}

        decisive_pct = 100.0 - match_stats["draw_pct"]

        print(f"   [Diagnostics] Matches: {match_stats['total_matches']} | Decisive: {decisive_pct:.1f}% | "
              f"Stagnant Draws: {match_stats['draw_pct']:.1f}% | Avg Winner Moves: {match_stats['avg_winner_moves']:.1f}")
        print(f"   [HoF Benchmark] Performance vs Titans: {hof_percentage:.1f}%")
        print(f"Gen {self.generation} Best -> {top_agent} (Fitness: {top_fitness:.1f})")
        print(f"   [Weights] {formatted_weights}")

        avg_fitness = sum(fit for _, fit in ranked_population) / len(ranked_population)

        # Record history for plotting
        self.history["generation"].append(self.generation)
        self.history["best_fitness"].append(top_fitness)
        self.history["avg_fitness"].append(avg_fitness)
        self.history["best_weights"].append(list(top_agent.weights))
        self.history["draw_pct"].append(match_stats["draw_pct"])
        self.history["avg_winner_moves"].append(match_stats["avg_winner_moves"])
        self.history["hof_benchmark_score"].append(hof_percentage)

        # Extract just the agent objects in order of fitness (best to worst)
        sorted_agents = [agent for agent, fitness in ranked_population]

        # 4. Elitism: Carry over the top N agents unchanged
        new_population = []
        for i in range(self.elite_count):
            elite_parent = sorted_agents[i]
            elite_clone = MinimaxAgent(
                name=f"Gen{self.generation + 1}_Elite_{i + 1}",
                weights=list(elite_parent.weights),
                depth=self.depth
            )
            new_population.append(elite_clone)

        # 5. Breed the rest of the population
        agent_counter = self.elite_count + 1
        while len(new_population) < self.population_size:
            parent_a = self._select_parent(ranked_population)
            parent_b = self._select_parent(ranked_population)

            child_weights = self._crossover(parent_a.weights, parent_b.weights)
            child_weights = self._mutate(child_weights)

            child_agent = MinimaxAgent(
                name=f"Gen{self.generation + 1}_Agent_{agent_counter}",
                weights=child_weights,
                depth=self.depth
            )
            new_population.append(child_agent)
            agent_counter += 1

        self.tournament_manager.population = new_population
        self.generation += 1
        return top_agent, top_fitness

    def _select_parent(self, ranked_population):
        pool_size = min(4, len(ranked_population))
        candidates = random.sample(ranked_population, pool_size)
        candidates.sort(key=lambda item: item[1], reverse=True)
        return candidates[0][0]

    def _crossover(self, weights_a, weights_b):
        child_weights = []
        for w_a, w_b in zip(weights_a, weights_b):
            chosen_weight = w_a if random.random() < 0.5 else w_b
            child_weights.append(chosen_weight)
        return child_weights

    def _mutate(self, weights):
        mutated_weights = []
        for w in weights:
            if random.random() < self.mutation_rate:
                noise = random.gauss(0, self.mutation_strength)
                new_w = max(0.1, w + noise)
                mutated_weights.append(new_w)
            else:
                mutated_weights.append(w)
        return mutated_weights