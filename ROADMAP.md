# 🗺️ Project Roadmap: Evolutionary Checkers AI

Welcome to the development roadmap for our PUCV AI Module 3 Checkers project. This document tracks our backlog of diagnostic tools, core mechanics adjustments, and future optimization milestones aimed at achieving robust strategy convergence.

---

## 🚀 Phase 1: Performance Optimization & Core Mechanics (Completed)
* **[x] Multi-Core Tournament Parallelization**
  * Utilized Python's `concurrent.futures.ProcessPoolExecutor` to distribute independent round-robin matches across multiple CPU cores, dramatically reducing per-generation wall-clock time.
* **[x] Adaptive Endgame Search Depth**
  * Dynamically scaled search depth up to 5 when total active board pieces drop to $\le 6$, closing the horizon gap in sparse endgames.
* **[x] Expanded Heuristic Feature Vector**
  * Integrated new tactical terms into the agent's evaluation function—including **Edge/Border Occupation Value** and **Endgame Proximity Hunting**—to enrich tactical diversity beyond the initial 4-parameter baseline.

---

## 📈 Phase 2: Advanced Evolutionary Scaling
* **[ ] Transposition Table Memoization**
  * Implement board-state hashing to cache evaluated subtrees during Minimax lookups, preventing redundant calculations across symmetric move orders.
* **[ ] Phase-Based Weight Profiles**
  * Explore splitting heuristic vectors into specialized early-, mid-, and end-game weight profiles triggered by piece-count state transitions.
* **[ ] Agent Library & Serialization**
  * Implement JSON/pickle export and import functions so trained champions can be saved to disk, loaded, and pitted against each other across sessions.

---

## 🖥️ Phase 3: Diagnostic GUI & Telemetry Studio (Long-Term)
* **[ ] Real-Time Tournament Leaderboard**
  * Display a live-updating scoreboard during round-robin evaluations showing ongoing W/D/L records, match tickers, and live fitness rankings.
* **[ ] Interactive Human vs. AI Mode**
  * Build a graphical board interface allowing a human player to select a saved named agent and play against it with legal move highlighting and forced-jump enforcement.

---

## ✅ Done

### 2026-10-14
* **Match Outcome Analytics:** Integrated automated telemetry into `tournament.py` to differentiate between decisive capture wins and timeout draws.
* **Anti-Stagnation Fitness Shaping:** Implemented severe move-count time-tax penalties for max-move draws and stripped win bonuses from stalled games, dropping stalemate rates from ~90% down to 0%–2%.
* **High-Mutation Evolutionary Tuning:** Scaled population and calibrated mutation parameters to successfully break local weight plateaus.
* **Multi-Core Tournament Parallelization:** Distributed round-robin evaluations across all CPU cores via `ProcessPoolExecutor`.
* **Adaptive Endgame Search Depth & Heuristic Expansion:** Implemented depth-5 endgame scaling, Edge/Border Occupation bonuses, and Endgame Proximity hunting gradients.
* **Dual-Axis Telemetry & Plotting:** Upgraded diagnostics to track draw percentages and winner move counts across timestamped, non-blocking high-resolution PNG exports.