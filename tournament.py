# tournament.py
import time
import os
import concurrent.futures
from agent import MinimaxAgent
from board import Board


def clear_screen():
    """Clears the terminal screen for a smooth visual animation effect."""
    os.system('cls' if os.name == 'nt' else 'clear')


class MatchStats:
    """Tracks game milestones and statistics for a single match."""

    def __init__(self):
        self.red_captures = 0
        self.blue_captures = 0
        self.red_kings_made = 0
        self.blue_kings_made = 0
        self.move_count = 0
        self.outcome = "Unknown"


class Match:
    """Encapsulates a single game between two Minimax agents with shaped fitness scoring and anti-draw penalties."""

    def __init__(self, ai_red, ai_blue, max_moves=150, verbose=False):
        self.ai_red = ai_red
        self.ai_blue = ai_blue
        self.max_moves = max_moves
        self.verbose = verbose
        self.board = Board()
        self.stats = MatchStats()

    def run(self):
        """Executes the game loop from start to finish and returns (red_fitness, blue_fitness, outcome_string)."""
        if self.verbose:
            print(f"=== CHECKERS: {self.ai_red} (Red) vs. {self.ai_blue} (Blue) ===")

        while not self.board.is_game_over() and self.stats.move_count < self.max_moves:
            if self.verbose:
                clear_screen()
                self.board.display()

            current_player = self.board.current_turn
            current_agent = self.ai_red if current_player == 1 else self.ai_blue

            if self.verbose:
                print(f"\nCurrent Turn: {current_agent} ({'Red' if current_player == 1 else 'Blue'})")
                print("AI is thinking...")

            ai_move = current_agent.get_move(self.board)

            if not ai_move:
                break

            self._process_move_milestones(ai_move, current_player)
            self.board.make_move(ai_move)
            self.stats.move_count += 1

            if self.verbose:
                time.sleep(0.1)

        if self.verbose:
            clear_screen()
            print("\n=== GAME OVER ===")
            self.board.display()

        return self._calculate_shaped_fitness()

    def _process_move_milestones(self, move, current_player):
        """Tracks captures and king promotions for shaped fitness."""
        if move.captures:
            if current_player == 1:
                self.stats.red_captures += len(move.captures)
            else:
                self.stats.blue_captures += len(move.captures)

        start_r, start_c = move.path[0]
        end_r, end_c = move.path[-1]
        piece = self.board.grid[start_r][start_c]

        is_promotion = (piece == 1 and end_r == 0) or (piece == -1 and end_r == 7)
        if is_promotion:
            if current_player == 1:
                self.stats.red_kings_made += 1
            else:
                self.stats.blue_kings_made += 1

    def _calculate_shaped_fitness(self):
        """Evaluates final board state and computes shaped fitness scores with severe anti-draw penalties."""
        red_pieces = 0
        blue_pieces = 0
        red_advancement = 0
        blue_advancement = 0

        for r in range(8):
            for c in range(8):
                p = self.board.grid[r][c]
                if p > 0:
                    red_pieces += 1
                    red_advancement += (7 - r)
                elif p < 0:
                    blue_pieces += 1
                    blue_advancement += r

        red_won = False
        blue_won = False
        is_draw = False

        if red_pieces > blue_pieces and blue_pieces == 0:
            red_won = True
            self.stats.outcome = "Red Win (Elimination)"
        elif blue_pieces > red_pieces and red_pieces == 0:
            blue_won = True
            self.stats.outcome = "Blue Win (Elimination)"
        elif self.stats.move_count >= self.max_moves or not self.board.get_legal_moves(self.board.current_turn):
            if red_pieces > blue_pieces:
                red_won = True
                self.stats.outcome = "Max-Moves / Red Advantage Win"
            elif blue_pieces > red_pieces:
                blue_won = True
                self.stats.outcome = "Max-Moves / Blue Advantage Win"
            else:
                is_draw = True
                self.stats.outcome = "Stalemate / True Draw"

        red_base = (
                (self.stats.red_captures * 6.0) +
                (self.stats.red_kings_made * 10.0) +
                (red_pieces * 3.0) +
                (red_advancement * 0.2)
        )

        blue_base = (
                (self.stats.blue_captures * 6.0) +
                (self.stats.blue_kings_made * 10.0) +
                (blue_pieces * 3.0) +
                (blue_advancement * 0.2)
        )

        if is_draw:
            red_fitness = red_base - (self.stats.move_count * 0.2)
            blue_fitness = blue_base - (self.stats.move_count * 0.2)
        else:
            red_fitness = red_base + (60.0 if red_won else -10.0) - (self.stats.move_count * 0.05)
            blue_fitness = blue_base + (60.0 if blue_won else -10.0) - (self.stats.move_count * 0.05)

        red_fitness = max(0.0, red_fitness)
        blue_fitness = max(0.0, blue_fitness)

        return red_fitness, blue_fitness, self.stats.outcome


def _run_single_match_worker(agent_pair):
    """Top-level helper function for ProcessPoolExecutor to execute two games between agent_a and agent_b."""
    agent_a, agent_b = agent_pair

    # Game 1: agent_a (Red) vs agent_b (Blue)
    match_1 = Match(agent_a, agent_b, verbose=False)
    fit_a1, fit_b1, outcome_1 = match_1.run()

    # Game 2: agent_b (Red) vs agent_a (Blue) - swap sides
    match_2 = Match(agent_b, agent_a, verbose=False)
    fit_b2, fit_a2, outcome_2 = match_2.run()

    # FIX: Use agent names as keys instead of object references
    scores = {
        agent_a.name: fit_a1 + fit_a2,
        agent_b.name: fit_b1 + fit_b2
    }
    outcomes = [outcome_1, outcome_2]
    return scores, outcomes


class TournamentManager:
    """Manages agent populations, matchups, and parallelized round-robin evaluation scoring."""

    def __init__(self, population_size=10, depth=3):
        self.population_size = population_size
        self.depth = depth
        self.population = self._initialize_population()

    def _initialize_population(self):
        import random
        population = []
        for i in range(self.population_size):
            weights = [
                random.uniform(5.0, 15.0),   # [0] Regular piece value
                random.uniform(15.0, 30.0),  # [1] King piece value
                random.uniform(0.0, 8.0),    # [2] Center control bonus
                random.uniform(0.0, 5.0),    # [3] Back-row defense bonus
                random.uniform(0.0, 5.0),    # [4] Edge / border occupation bonus
                random.uniform(0.0, 5.0)     # [5] Endgame proximity / hunting bonus
            ]
            name = f"Agent_{i+1}"
            population.append(MinimaxAgent(name=name, weights=weights, depth=self.depth))
        return population

    def run_round_robin(self):
        # Create a lookup dictionary from name -> agent object
        name_to_agent = {agent.name: agent for agent in self.population}
        fitness_scores = {agent: 0.0 for agent in self.population}
        match_counts = {agent: 0 for agent in self.population}
        outcomes_log = {"Elimination": 0, "Max-Move / Stagnation": 0}

        # Build pair tasks for all unique combinations (Round Robin)
        tasks = []
        n = len(self.population)
        for i in range(n):
            for j in range(i + 1, n):
                tasks.append((self.population[i], self.population[j]))

        # Execute matches in parallel across all CPU cores
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(_run_single_match_worker, tasks)

            for scores, outcomes in results:
                for agent_name, score in scores.items():
                    agent = name_to_agent[agent_name]  # Resolve back to original object
                    fitness_scores[agent] += score
                    match_counts[agent] += 2  # 2 games per pair matchup

                for outcome in outcomes:
                    if "Elimination" in outcome or "Advantage Win" in outcome:
                        outcomes_log["Elimination"] += 1
                    else:
                        outcomes_log["Max-Move / Stagnation"] += 1

        total_matches = sum(outcomes_log.values())
        if total_matches > 0:
            elim_pct = (outcomes_log["Elimination"] / total_matches) * 100
            draw_pct = (outcomes_log["Max-Move / Stagnation"] / total_matches) * 100
            print(
                f"   [Diagnostics] Matches: {total_matches} | Decisive / Advantage: {elim_pct:.1f}% | Stagnant Draws: {draw_pct:.1f}%")

        averaged_fitness = {
            agent: (fitness_scores[agent] / match_counts[agent]) if match_counts[agent] > 0 else 0.0
            for agent in self.population
        }

        ranked_population = sorted(averaged_fitness.items(), key=lambda item: item[1], reverse=True)
        return ranked_population