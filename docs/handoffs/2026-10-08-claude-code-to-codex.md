# Handoff

## Author and intended reviewer

Author: Claude Code. Intended reviewer: Codex. Rahan approves all changes and must confirm before Codex acts on this note.

## Task / issue

Propose a polling source for all-state 2022 and 2024 Senate general elections, so the error-model calibration can cover more than two cycles. This is a source proposal only; no collection until Rahan approves it in docs/data_sources.md.

## Branch and commit

main at 10e8715, plus the commit that adds this note (Rahan's notebook calibration cells, Decision 016, STATUS.md and file guide updates).

## Data snapshot / checksum

- Prepared calibration inputs: data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1/.
- Polling archive: data/raw/texas_senate_historical/20261006T024116Z/senate_polls_historical.csv contains 2018 (2,019 candidate rows) and 2020 (2,574) only.
- Results: data/raw/senate_results/20261006T035630Z/ (MEDSL V8.0) already includes all 2024 Senate returns; contests.csv lists 34 outside-scope 2024 rounds.

## Relevant files

docs/decisions.md (Decisions 012, 014, 016), docs/data_sources.md, docs/calibration_preparation_plan.md, data/processed/senate_calibration/README.md.

## What changed

Rahan ran the first calibration (notebooks/data-pulls.ipynb) on the 52 eligible contests with selected polls. Claude Code reproduced it independently with the same result. Live rules, h = 14:

| Horizon (days) | Races | Mean error (D − R) | RMSE (σ) |
| --- | ---: | ---: | ---: |
| 7 | 50 | −2.84 | 6.50 |
| 14 | 50 | −3.16 | 6.80 |
| 28 | 50 | −3.87 | 7.03 |
| 42 | 47 | −3.10 | 6.45 |

Mean error by cycle is about −0.1 to −1.8 (2018), −4.8 to −6.5 (2020) and about −5 (Texas 2024, one race). The cycle-wide lean is the largest part of σ, and it is estimated from essentially two cycles. More cycles are the most direct way to make σ less fragile.

## Decisions already approved by Rahan

Decisions 001–016. Decision 016 keeps σ = RMSE with no bias correction. Decision 012's calibration scope (all 2018/2020 races plus Texas 2024) is unchanged until Rahan approves an expansion; Rahan has asked for this proposal to inform that decision.

## Checks performed and observed results

- 197 race × horizon errors plus 11 dropped (no polls before the horizon) = 52 × 4. Dropped: Wyoming 2018 and 2020 at all horizons; DE, OR, WV 2020 at 42 days.
- Texas check: 2018 error about +3 (O'Rourke beat his polls); 2024 about −5.

## Checks not performed

No 2022/2024 polling source has been examined for availability, coverage or licensing.

## Open questions / concerns

- FiveThirtyEight's live poll files covered 2022 and 2024, but 538 was shut down in 2025. Current availability, archived mirrors, and whether the CC BY 4.0 terms still apply need checking.
- Whether to include 2022 as well as 2024 is Rahan's call; propose both, with coverage counts for each.
- Partisan/internal tags and population labels are needed to apply Decisions 012 and 013 consistently with the 2018/2020 archive.

## Requested next action

For Codex, after Rahan confirms:

1. Propose one or more sources for all-state 2022 and 2024 Senate general-election polls, with access method, license/redistribution terms, field coverage (fieldwork dates, population, sample size, pollster, sponsor, partisan/internal flags, candidate-level shares, question IDs) and approximate counts by cycle.
2. Note 2022 election-results coverage: MEDSL V8.0 is approved for 2018/2020/2024 only (Decision 014), so 2022 would need either approval of the same source for 2022 or another source.
3. Describe how the existing preparer (src/clean/prepare_senate_calibration.py) would extend to the new cycles: side mapping, exact-round crosswalk, Georgia 2022 runoff, any same-party or independent-candidate cases (for example Utah 2022, McMullin), and list them for Rahan rather than resolving them.
4. Do not collect until Rahan approves the source in docs/data_sources.md.

Do not compute margins, averages, errors, σ or probabilities (Decision 001).

## What Rahan should implement or explain

- Decide whether to expand the calibration scope to 2024, and possibly 2022, once the proposal arrives.
- No notebook changes are needed for expansion: the calibration loop picks up the new contests from the prepared files.
