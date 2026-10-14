# Changelog

All notable changes and experimental findings for the Evolutionary Checkers AI project will be documented in this file.

## [Unreleased] - 2026-10-14
### Added
- **Match Outcome Diagnostics:** Integrated automated telemetry into `tournament.py` to differentiate between decisive capture wins and timeout draws[cite: 7].
- **Anti-Stagnation Fitness Shaping:** Implemented severe move-count time-tax penalties for max-move draws and stripped win bonuses from stalled games to force aggressive play[cite: 7].
- **High-Mutation Evolutionary Run:** Scaled population to 20 and tuned mutation rate ($0.35$) and strength ($2.5$) across a 20-generation training cycle (380 matches/gen).

### Findings & Insights
- **Stagnation Confirmed:** Diagnostic logs across early evolutionary runs revealed that 76% to 100% of tournament matches end in max-move stalemates by Generation 3+[cite: 7]. 
- **Root Cause Identified:** The original fitness function unintentionally rewarded passive material hoarding and survival over aggressive play, causing Depth-3 agents to evolve defensive stalling strategies[cite: 7].
- **Stagnation Successfully Resolved:** Introducing anti-draw fitness shaping dropped max-move stagnation rates from ~90% down to a steady 4%–15%, successfully forcing populations toward decisive, elimination-heavy matches.
- **Heuristic Stabilization & Center Deprecation:** Across 20 generations of high-mutation pressure, regular/king piece valuations stabilized (maintaining proper hierarchy around 14 and 21–26 respectively), while Center Control weights dropped to near-zero ($0.1$), indicating it provides negligible tactical advantage at Depth 3.