# Changelog

All notable changes and experimental findings for the Evolutionary Checkers AI project will be documented in this file.

## [Unreleased] - 2026-10-14
### Added
- **Match Outcome Diagnostics:** Integrated automated telemetry into `tournament.py` to differentiate between decisive capture wins and timeout draws.
- **Anti-Stagnation Fitness Shaping:** Implemented severe move-count time-tax penalties for max-move draws and stripped win bonuses from stalled games to force aggressive play.
- **Multi-Core Parallel Tournament Evaluation:** Integrated `concurrent.futures.ProcessPoolExecutor` to distribute round-robin match pairings across all available CPU cores.
- **Edge/Border Occupation Heuristic:** Expanded feature vector to include outer-column sanctuary bonuses, establishing a tactical competition between center control and edge defense.
- **Endgame Proximity Hunting & Adaptive Depth:** Added an opponent-proximity gradient feature and dynamic depth scaling (boosting search depth to 5 when total board pieces drop to $\le 6$) to eliminate late-game blindness.

### Findings & Insights
- **Stagnation Successfully Erased:** Anti-draw shaping combined with expanded positional heuristics successfully pushed decisive match outcomes to a consistent **95%–99.7%**, keeping stalemate rates below 5%.
- **Active Genetic Divergence:** Multi-generation runs show strong selective pressure on back-row defense and endgame hunting weights, demonstrating that the GA is actively discovering distinct tactical styles (e.g., heavy defensive anchoring vs. aggressive endgame pursuit).
- **Performance Balance:** Offloading round-robin evaluations to all CPU cores maintains highly efficient generation times (30–60 seconds) even with adaptive Depth-5 endgame searches engaged.