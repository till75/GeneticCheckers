import json
import os
from agent import MinimaxAgent


class HallOfFame:
    def __init__(self, max_size=5):
        self.archive = []  # Stores dicts with generation, agent, and weights
        self.max_size = max_size

    def add_champion(self, generation: int, agent: MinimaxAgent, benchmark_percentage: float = None):
        """Adds a generation's best agent to the Hall of Fame only if it sets a true record or passes a high benchmark."""
        champ_data = {
            "generation": generation,
            "weights": agent.weights.copy(),
            "fitness": agent.fitness
        }

        # PROTECTION: If an archive has pre-seeded titans, don't let early weak gens
        # overwrite them just because they won a local round-robin.
        # Require them to either beat the absolute best titan OR score > 75% against the HoF.
        is_absolute_record = not self.archive or agent.fitness > self.archive[0]["fitness"]
        is_proven_titan = benchmark_percentage is not None and benchmark_percentage >= 75.0

        if is_absolute_record or (len(self.archive) < self.max_size and is_proven_titan):
            self.archive.append(champ_data)
            self.archive.sort(key=lambda x: x["fitness"], reverse=True)
            if len(self.archive) > self.max_size:
                self.archive.pop()
            print(f"   [HoF] Milestone Achieved! Gen {generation} added to archive (Fitness: {agent.fitness:.1f})")
        else:
            print(f"   [HoF Guard] Gen {generation} champion (Fitness: {agent.fitness:.1f}) did not surpass historical titans.")

    def get_benchmark_agents(self, depth: int) -> list[MinimaxAgent]:
        """Instantiates and returns MinimaxAgents for all HoF members."""
        benchmarks = []
        for entry in self.archive:
            agent = MinimaxAgent(
                name=f"HoF_Gen_{entry['generation']}",
                weights=entry["weights"],
                depth=depth
            )
            benchmarks.append(agent)
        return benchmarks

    def save_to_disk(self, filepath="hall_of_fame.json", read_only=False):
        """Serializes the HoF archive to disk for persistent tracking."""
        if read_only:
            print("   [HoF] Archive is locked. Skipping save.")
            return

        with open(filepath, "w") as f:
            json.dump(self.archive, f, indent=4)

    def load_from_disk(self, filepath="hall_of_fame.json"):
        """Loads a saved Hall of Fame archive from disk."""
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                self.archive = json.load(f)