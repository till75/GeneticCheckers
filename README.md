### Project Description

An open-source Checkers engine and evolutionary framework written in Python, developed as the final project for Module 3 of the Diplomado en Inteligencia Artificial at Pontificia Universidad Católica de Valparaíso (PUCV). The project uses a Minimax search algorithm with Alpha-Beta pruning to evaluate game trees and simulate match outcomes between AI agents. Rather than relying on static, hand-tuned evaluation functions, the system employs a Co-Evolutionary Genetic Algorithm (GA) to automatically discover and optimize heuristic weight vectors for material balance, king valuation, center control, and back-row defense. Evaluated through two-game round-robin tournaments with side swapping, agents adapt iteratively across generations without human supervision. Google Gemini served as an AI pair programmer throughout development—assisting in architecture design, debugging Minimax recursion and terminal dashboard integration, analyzing evolutionary convergence metrics, and documenting project specifications. The execution pipeline tracks fitness progression, logs weight convergence, and renders dual-panel Matplotlib figures at the conclusion of training runs. Designed with clean modularity, it provides a solid foundation for future interactive menu integration, live graphical tournament dashboards, and human-vs-AI gameplay.

---

### Key Modules

* **`board.py`**
Handles 8x8 checkerboard state representations, legal step/jump move generation, mandatory capture enforcement, and king promotions.


* **`agent.py`**
Implements the `MinimaxAgent` engine featuring recursive search, Alpha-Beta pruning, depth tie-breaking, and multi-feature state evaluation.


* **`tournament.py` (`Match`, `TournamentManager`)**
Encapsulates individual game execution with shaped fitness scoring and manages full round-robin tournament schedules across the agent population.


* **`genetic.py` (`GeneticAlgorithm`)**
Drives evolutionary generation cycles through round-robin evaluation, elite cloning, tournament selection, uniform crossover, and Gaussian weight mutation.


* **`main.py`**
Serves as the entry point script that configures hyperparameters, executes the genetic evolutionary loop, and plots fitness/weight trajectories.