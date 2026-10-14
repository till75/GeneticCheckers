# tournament.py
import time
import os
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


class Match:
    """Encapsulates a single game between two Minimax agents with shaped fitness scoring."""
    def __init__(self, ai_red, ai_blue, max_moves=150, verbose=False):
        self.ai_red = ai_red
        self.ai_blue = ai_blue
        self.max_moves = max_moves
        self.verbose = verbose
        self.board = Board()
        self.stats = MatchStats()

    def run(self):
        """Executes the game loop from start to finish and returns (red_fitness, blue_fitness)."""
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
                # No legal moves means the current player loses
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

        if self.verbose:
            print(f"AI chose move path: {move.path}")

    def _calculate_shaped_fitness(self):
        """Evaluates final board state, tie-breaks, and computes shaped fitness scores."""
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

        # Determine win/loss status
        red_won = False
        blue_won = False

        if red_pieces > blue_pieces and blue_pieces == 0:
            red_won = True
        elif blue_pieces > red_pieces and red_pieces == 0:
            blue_won = True
        elif self.stats.move_count >= self.max_moves or not self.board.get_legal_moves(self.board.current_turn):
            red_tie_score = (red_pieces * 10) + (red_advancement * 0.5)
            blue_tie_score = (blue_pieces * 10) + (blue_advancement * 0.5)
            if red_tie_score >= blue_tie_score:
                red_won = True
            else:
                blue_won = True

        # Shaped fitness formula combining milestones and outcome bonuses
        red_fitness = (
            (50.0 if red_won else 0.0) +
            (self.stats.red_captures * 5.0) +
            (self.stats.red_kings_made * 8.0) +
            (red_pieces * 3.0) +
            (red_advancement * 0.2)
        )

        blue_fitness = (
            (50.0 if blue_won else 0.0) +
            (self.stats.blue_captures * 5.0) +
            (self.stats.blue_kings_made * 8.0) +
            (blue_pieces * 3.0) +
            (blue_advancement * 0.2)
        )

        if self.verbose:
            print(f"\n--- Match Statistics ---")
            print(f"Red ({self.ai_red})  -> Captures: {self.stats.red_captures}, Kings: {self.stats.red_kings_made}, Fitness: {red_fitness:.1f}")
            print(f"Blue ({self.ai_blue}) -> Captures: {self.stats.blue_captures}, Kings: {self.stats.blue_kings_made}, Fitness: {blue_fitness:.1f}")

        return red_fitness, blue_fitness


class TournamentManager:
    """Manages agent populations, matchups, and round-robin evaluation scoring."""
    def __init__(self, population_size=10, depth=3):
        self.population_size = population_size
        self.depth = depth
        self.population = self._initialize_population()

    def _initialize_population(self):
        """Creates an initial population of agents with randomized heuristic weights."""
        import random
        population = []
        for i in range(self.population_size):
            weights = [
                random.uniform(5.0, 15.0),   # Regular piece value
                random.uniform(15.0, 30.0),  # King piece value
                random.uniform(0.0, 8.0),    # Center control bonus
                random.uniform(0.0, 5.0)     # Back-row defense bonus
            ]
            name = f"Agent_{i+1}"
            population.append(MinimaxAgent(name=name, weights=weights, depth=self.depth))
        return population

    def run_round_robin(self):
        """
        Runs a round-robin tournament where every agent plays every other agent
        twice (swapping sides) to ensure a fair, unbiased fitness ranking.
        """
        fitness_scores = {agent: 0.0 for agent in self.population}
        match_counts = {agent: 0 for agent in self.population}

        n = len(self.population)
        for i in range(n):
            print(f"Evaluating Agent {self.population[i]} in tournament matches...")
            for j in range(i + 1, n):
                agent_a = self.population[i]
                agent_b = self.population[j]

                # --- Game 1: Agent A is Red, Agent B is Blue ---
                match_1 = Match(agent_a, agent_b, verbose=False)
                fit_a1, fit_b1 = match_1.run()
                fitness_scores[agent_a] += fit_a1
                fitness_scores[agent_b] += fit_b1
                match_counts[agent_a] += 1
                match_counts[agent_b] += 1

                # --- Game 2: Swap sides (Agent B is Red, Agent A is Blue) ---
                match_2 = Match(agent_b, agent_a, verbose=False)
                fit_b2, fit_a2 = match_2.run()
                fitness_scores[agent_a] += fit_a2
                fitness_scores[agent_b] += fit_b2
                match_counts[agent_a] += 1
                match_counts[agent_b] += 1

        # Average the fitness scores based on total matches played
        averaged_fitness = {
            agent: (fitness_scores[agent] / match_counts[agent]) if match_counts[agent] > 0 else 0.0
            for agent in self.population
        }

        # Sort population descending by fitness
        ranked_population = sorted(averaged_fitness.items(), key=lambda item: item[1], reverse=True)
        return ranked_population