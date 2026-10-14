# 🗺️ Project Roadmap: Evolutionary Checkers AI

Welcome to the development roadmap for our PUCV AI Module 3 Checkers project. This document tracks our backlog of diagnostic tools, core mechanics adjustments, and future optimization milestones aimed at achieving robust strategy convergence.

---

## 🚀 Phase 1: Performance Optimization & Core Mechanics (Next Steps)
* **[ ] Multi-Core Tournament Parallelization**  
  * Use Python's `concurrent.futures.ProcessPoolExecutor` to distribute independent round-robin matches across multiple CPU cores, dramatically reducing per-generation wall-clock time.
* **[ ] Adaptive Endgame Search Depth**  
  * Dynamically scale search depth up (e.g., from Depth 3 to 4 or 5) when total active board pieces drop below a threshold ($\le 8$), closing the horizon gap in sparse endgames.
* **[ ] Expanded Heuristic Feature Vector**  
  * Integrate new tactical terms into the agent's evaluation function—such as **Edge/Border Occupation Value** (side-rail anchoring) and **Promotion Proximity** (forward marching bonus)—to enrich tactical diversity beyond the 4-parameter baseline.

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
* **Anti-Stagnation Fitness Shaping:** Implemented severe move-count time-tax penalties for max-move draws and stripped win bonuses from stalled games, dropping stalemate rates from ~90% down to 0%–15%.
* **High-Mutation Evolutionary Tuning:** Scaled population to 20 and calibrated mutation rate ($0.35$) and strength ($2.5$) to successfully break local weight plateaus.