# Changelog

All notable changes and experimental findings for the Evolutionary Checkers AI project will be documented in this file.

## [Unreleased] - 2026-10-14
### Added
- **Match Outcome Diagnostics:** Integrated automated telemetry into `tournament.py` to differentiate between decisive capture wins and timeout draws.
- **Anti-Stagnation Fitness Shaping:** Implemented severe move-count time-tax penalties for max-move draws and stripped win bonuses from stalled games to force aggressive play.
- **High-Mutation Evolutionary Run:** Scaled population to 20 and tuned mutation rate ($0.35$) and strength ($2.5$) across multi-generation training cycles.
- **Multi-Core Parallel Tournament Evaluation:** Integrated `concurrent.futures.ProcessPoolExecutor` to distribute round-robin match pairings across all available CPU cores.

### Findings & Insights
- **Stagnation Confirmed:** Diagnostic logs across early evolutionary runs revealed that 76% to 100% of tournament matches ended in max-move stalemates by Generation 3+. 
- **Root Cause Identified:** The original fitness function unintentionally rewarded passive material hoarding and survival over aggressive play, causing Depth-3 agents to evolve defensive stalling strategies.
- **Stagnation Successfully Resolved:** Introducing anti-draw fitness shaping dropped max-move stagnation rates from ~90% down to a steady 12%–20%, successfully forcing populations toward decisive, elimination-heavy matches.
- **Massive Performance Gain:** Offloading round-robin evaluations to multi-processing workers reduced generation wall-clock time from ~190–250 seconds down to **17–24 seconds**, fully saturating available CPU threads and unlocking rapid iterative experimentation.