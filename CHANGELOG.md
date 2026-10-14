# Changelog

All notable changes and experimental findings for the Evolutionary Checkers AI project will be documented in this file.

## [Unreleased] - 2026-10-14
### Added
- **Match Outcome Diagnostics:** Integrated automated telemetry into `tournament.py` to differentiate between decisive capture wins and timeout draws.
- **Anti-Stagnation Fitness Shaping:** Implemented severe move-count time-tax penalties for max-move draws and stripped win bonuses from stalled games to force aggressive play.

### Findings & Insights
- **Stagnation Confirmed:** Diagnostic logs across early evolutionary runs revealed that 76% to 100% of tournament matches end in max-move stalemates by Generation 3+. 
- **Root Cause Identified:** The original fitness function unintentionally rewarded passive material hoarding and survival over aggressive play, causing Depth-3 agents to evolve defensive stalling strategies.
- **Stagnation Successfully Resolved:** Introducing anti-draw fitness shaping dropped max-move stagnation rates from ~90% down to 0%–2%, successfully forcing populations toward decisive, elimination-heavy matches.
- **Local Optimum Convergence:** While game play is now active and decisive, heuristic weight trajectories stabilized rapidly by Generation 2, indicating that the 4-parameter vector at Depth 3 quickly reaches a plateau.