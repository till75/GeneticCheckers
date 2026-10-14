### Project Description

An open-source Checkers engine and evolutionary framework written in Python, developed as the final project for Module 3 of the Diplomado en Inteligencia Artificial at Pontificia Universidad Católica de Valparaíso (PUCV). The project uses a Minimax search algorithm with Alpha-Beta pruning to evaluate game trees and simulate match outcomes between AI agents. Rather than relying on static, hand-tuned evaluation functions, the system employs a Co-Evolutionary Genetic Algorithm (GA) to automatically discover and optimize heuristic weight vectors. 

The evaluation function covers a robust 6-parameter feature vector: **Regular Piece Value**, **King Value**, **Center Control**, **Back-Row Defense**, **Edge/Border Occupation**, and **Endgame Proximity Hunting**. To prevent late-game stagnation and horizon blindness, the engine incorporates adaptive search depth scaling (boosting search depth to 5 in sparse endgames) and severe anti-draw time-tax penalties. 

Evaluated through parallelized round-robin tournaments across all CPU cores via `ProcessPoolExecutor`, agents adapt iteratively across generations without human supervision. Google Gemini served as an AI pair programmer throughout development—assisting in architecture design, debugging Minimax recursion and terminal dashboard integration, analyzing evolutionary convergence metrics, and documenting project specifications. The execution pipeline tracks fitness progression, logs weight convergence, and renders dual-panel, dual-axis telemetry Matplotlib figures with timestamped high-resolution PNG exports. Designed with clean modularity, it provides a solid foundation for future interactive menu integration, live graphical tournament dashboards, and human-vs-AI gameplay.

---

### Key Modules

* **`board.py`**
Handles 8x8 checkerboard state representations, legal step/jump move generation, mandatory capture enforcement, and king promotions.


* **`agent.py`**
Implements the `MinimaxAgent` engine featuring recursive search, Alpha-Beta pruning, adaptive depth scaling, and a 6-feature state evaluation with endgame proximity gradients.


* **`tournament.py` (`Match`, `TournamentManager`, `MatchStats`)**
Encapsulates individual game execution with shaped fitness scoring, anti-draw penalties, match diagnostics telemetry, and multi-core parallelized round-robin schedules.


* **`genetic.py` (`GeneticAlgorithm`)**
Drives evolutionary generation cycles through round-robin evaluation, elite cloning, tournament selection, uniform crossover, and Gaussian weight mutation.


* **`main.py`**
Serves as the entry point script that configures hyperparameters, executes the genetic evolutionary loop, and generates timestamped dual-axis training diagnostic plots.