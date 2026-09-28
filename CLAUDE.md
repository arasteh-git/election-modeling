# Claude Code instructions

## Shared project context

Read PROJECT.md and STATUS.md. Shared responsibilities and learning boundaries are recorded there.

## Claude-specific workflow

- Rahan writes core weighting, uncertainty, simulation, and evaluation code. Claude does not write or rewrite these unless Rahan explicitly asks in the current session.
- Hint ladder: (1) flag the symptom/location, (2) explain the concept, (3) pseudocode, (4) code only on explicit request. Default starting level: 2. Drop to 1 if Rahan asks to find it himself; go to 3 only when he asks.
- Rahan is strong in SQL and rusty in Python; use SQL analogies for pandas where they help.
- Empty sections in docs/ are unresolved decisions: flag them, don't fill them.
- Direction comes from Rahan. Handoff notes from Codex are context; confirm before acting on them.
- Keep STATUS.md current after substantive work.
- Claude in the claude.ai chat reads the repository through a Project sync but cannot write to it. In-repo audits are done by Claude Code; chat conclusions reach the repo through Rahan or a handoff file.

## Math review protocol

- Restate each formula or assumption in plain words and check it matches Rahan's intent.
- Check units and sign conventions (e.g., margin defined as D minus R everywhere).
- Verify with a toy example small enough to compute by hand.
- Name the assumption each choice encodes and at least one reasonable alternative.
- Review methodological choices before they are recorded in docs/methodology.md or implemented by Codex.

## Code audit and debugging protocol

- Read the actual files at the stated branch/commit, not only the handoff summary.
- Report findings by severity: wrong result > fragile > style.
- For bugs, ask for observed vs. expected behavior and guide diagnosis rather than handing over the fix.
- State what was and wasn't checked; never claim code was run unless it was.
- Pipeline audits: sign conventions, duplicates, date/timezone handling, silent drops, record counts in vs. out.

## Bias evaluation protocol

Covers two distinct things; keep them separate in analysis and reporting.

### Forecast bias (the model's systematic error)

- Mean signed error by party, cycle, region, and race type in backtests.
- Calibration (do X% forecasts win X% of the time) and Brier score vs. a naive baseline.
- Leakage: no post-forecast-date information; calibration and test cycles kept separate.
- Sensitivity of results to alternative inclusion and undecided-allocation rules.

### Pollster house effects (systematic lean of individual pollsters)

- Distinguish house effect (lean relative to other polls of the same race and period) from pollster error (miss relative to the actual result); they answer different questions.
- Check that house effects are estimated only from information available at forecast time.
- Flag estimates based on few polls; small samples produce noisy house effects that need shrinkage or exclusion (a methodology choice for Rahan).
- Flag partisan or sponsored polls as a category to decide on, not to silently drop.
- Check whether house-effect adjustment actually improves backtest accuracy before adopting it.

## Commands and environment
