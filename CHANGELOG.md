# Changelog

All notable changes and experimental findings for the Evolutionary Checkers AI project will be documented in this file.

## [Unreleased] - 2026-10-14
### Added
- **Match Outcome Diagnostics:** Integrated automated telemetry into `tournament.py` to differentiate between decisive capture wins and timeout draws.

### Findings & Insights
- **Stagnation Confirmed:** Diagnostic logs across early evolutionary runs revealed that 76% to 100% of tournament matches end in max-move stalemates by Generation 3+. 
- **Root Cause Identified:** The current fitness function unintentionally rewards passive material hoarding and survival over aggressive play, causing Depth-3 agents to evolve defensive stalling strategies.