# 🗺️ Project Roadmap: Evolutionary Checkers AI

Welcome to the development roadmap for our PUCV AI Module 3 Checkers project. This document tracks our backlog of diagnostic tools, core mechanics adjustments, and future GUI features aimed at overcoming evolutionary stagnation.

---

## 🔍 Phase 1: Diagnostics & Fitness Landscape (Immediate Focus)
* **[ ] Match Outcome Analytics**  
  * Log and display game termination reasons in tournaments (e.g., capture win vs. max-move draw) to diagnose if stalemate vacillation is causing evolutionary stagnation.
* **[ ] Anti-Stagnation Fitness Shaping**  
  * Refactor the shaped fitness function in `tournament.py` to heavily penalize draw states or long, low-action games, forcing selection pressure toward aggressive tactical play.
* **[ ] Unbiased Parameter Space & Weight Bounds**  
  * Normalize initial weight bounds to a `[0.0, 1.0]` real number space to let co-evolution discover relative hierarchies unprompted.

---

## 🖥️ Phase 2: Diagnostic GUI & Telemetry Studio
* **[ ] Real-Time Tournament Leaderboard**  
  * Display a live-updating scoreboard during round-robin evaluations showing ongoing W/D/L records, match tickers, and live fitness rankings.
* **[ ] Inter-Generation Mutation & Genetic Lottery View**  
  * Visualize the evolutionary step between generations—highlighting surviving elites, parent crossover blending, and Gaussian weight mutations.
* **[ ] Interactive Human vs. AI Mode**  
  * Build a graphical board interface allowing a human player to select a saved named agent and play against it with legal move highlighting and forced-jump enforcement.

---

## 🚀 Phase 3: Advanced Mechanics & Persistence
* **[ ] Multi-Core Parallelization**  
  * Use Python's `multiprocessing` or `concurrent.futures` to execute independent round-robin tournament matches across multiple CPU cores.
* **[ ] Expanded Heuristic Strategy Search**  
  * Introduce advanced strategic evaluation terms, such as edge/border occupation penalties or phase-based weights (early vs. mid vs. end game) to break simple heuristic loops.
* **[ ] Agent Library & Serialization**  
  * Implement JSON/pickle export and import functions so trained champions can be saved to disk, loaded, and pitted against each other across sessions.

---

## 📌 Misc (Additional Ideas & Visualizations)
* **[ ] Pedigree & Survival Tree Visualization**  
  * Render a tree-like lineage graph tracking champion ancestry across generations to identify which genetic features survive over time.
* **[ ] Color-Coded Genetic Markers**  
  * Establish a visual color mapping (e.g., `0.0` Blue, `0.5` Purple, `1.0` Red) for weight values to make genetic recombinations and strategy clustering instantly identifiable at a glance.