# Project status

## Current milestone

Review the election-results source proposal and all-state preparation plan under Decision 012; then prepare inputs for Rahan's uncertainty-model calibration.

## Completed

- Agreed on the division of responsibilities between Rahan, ChatGPT/Codex, and Claude/Claude Code.
- Created the initial documentation and directory scaffold.
- Left unselected scope, methodology, data sources, and environment settings blank.
- Created the private GitHub repository and connected it to the Claude chat Project (read-only sync).
- Filled CLAUDE.md with the tutoring and review workflow (Decision 004).
- Onboarded Claude Code (NEXT_STEPS step 4): it summarized its boundaries and audited the scaffold against the 2026-09-27 handoff.
- Applied audit follow-ups:
  - CLAUDE.md now tells Claude to keep STATUS.md current.
  - README.md documents docs/handoffs/.
  - Decision 003 wording now reflects the repository connection.
- Tracked all of data/ in Git (Decision 005).
- .gitignore now covers key and credential files and .idea/; .idea/ was removed from tracking.

- Confirmed Codex repository access through the GitHub connector.
- Confirmed Senate races as the current focus; House modeling is deferred.

- Selected the Texas Politics Project tracker as the first Texas collection source (Decision 007).
- Extracted 16 tracker rows into a reproducible timestamped source snapshot and CSVs; recorded a spread discrepancy and primary-review limits.

- Added a file-by-file guide, expanded relevant folder READMEs, and recorded the standing README-maintenance rule.

- Claude Code reviewed the Codex Texas handoff and snapshot. Counts, checksum, and candidate-to-party mapping check out. It found that row 14 (UT/TPP, June) sums to 95%, alongside the known row 6 AARP spread mismatch.
- Rahan verified row 14 against its release. Candidate shares are correct; the tracker's Other column understates undecided and other responses. The snapshot is unchanged, and the row is RV, so it is excluded (see docs/texas_tracker_review.md).
- Rahan accepted the row 6 AARP spread mismatch as rounding. Margins use dem_pct minus rep_pct, not the tracker Spread (Decision 009).
- Selected Texas as the first race; Georgia and Michigan are tentative next races (Decision 006).
- Set the forecast target (win probability) and timeline: pre-election goal, backtest fallback (Decision 008).
- Approved the first Texas poll rules (Decision 009): LV only, labels as reported, repeat polls as separate observations, undecided left as reported, fieldwork end date, recency weighting. Recorded in docs/methodology.md.
- Rahan wrote the first LV-only, recency-weighted Texas average in notebooks/data-pulls.ipynb: +2.64 D − R with n_eff 5.48 at a working half-life of 14 days (Decision 009). Claude checked the results independently. Sensitivity for h = 7 and 30 is in docs/methodology.md.
- Defined the minimum deliverable and tiers (Decision 010): Texas P(Democrat wins) first; fundamentals and house effects next; correlation and P(Democrats win the Senate) last.

- Collected a historical Texas Senate inventory on 2026-10-05 at Rahan's request: 49 2018 questions, 63 2020 questions, and 37 2024 tracker rows, with all populations retained. Saved original sources, provenance/checksums, per-cycle CSVs, and mechanical flags.
- Verified candidate-row preservation, schema rejection, flag retention, byte-identical offline replay, and overwrite rejection. No historical primary releases verified.

- Applied Rahan-approved historical preparation (Decision 011): set all 37 2024 election dates to 2024-11-05, tag older source partisanship, and exclude the 12 hypothetical 2020 matchups from processed outputs. Retained 137 records (49/51/37), including 24 source-tagged partisan records; source flags remain preserved. Changes and exclusions are audited; raw snapshots remain unchanged.
- Five historical-preparation regression tests passed, checking exact exclusions, field preservation, date corrections, classifications/unknowns, ambiguous candidate retention, conflicting-date rejection, provenance hashes, and overwrite protection.

- Researched election-result sources and wrote `docs/calibration_preparation_plan.md` (2026-10-05): proposed MEDSL Senate V8.0/CC0 for 2018/2020 and Texas 2024, with official crosschecks, access/permission limits, output plan, and unresolved race rules. Metadata and codebook inspected; no result dataset saved or prepared. No source or new inclusion rule approved.
- Inspected the saved national polling archive: 4,593 candidate rows, 1,913 questions, 65 general race IDs and seven jungle/runoff IDs (72 race/stage groups, not independent seat outcomes). Flagged wider partisan labels, Maine 2018 RCV-reallocated rows, and a Louisiana apparent-runoff question without an election date. Raw data and the notebook were preserved.

- Recorded the calibration race-format rules (Decision 013) and σ = RMSE of errors (Decision 012), 2026-10-05.

## Not yet done

- Local Python environment setup.
- Approval of an election-results source (proposal ready; Decision 012). Calibration rules are set; the error-model form (e.g., normal vs. t distribution) is still undecided.
- Implementation of results collection and all-state preparation after approval. Decision 013 settles independents, same-party races, sum-by-party margins, and specials/runoffs. Still open: no-DEM contests, multiple rounds per seat, denominator, LIB/`REP,REF` partisan labels, general non-nominee exclusion, and multiple LV questions per poll.
- Open poll rule: LV numbers from releases where the tracker shows RV.
- Uncertainty model for win probability, and the baseline.
- Complete primary-source verification, analytical data cleaning, modeling, and evaluation.

## Next action

Rahan: review `docs/calibration_preparation_plan.md` and select the results source (recommended MEDSL V8.0 with official crosschecks). Source approval enables an immutable download and row-level coverage audit; approve the relevant unresolved preparation rules before analytical filtering. Codex then prepares the approved inputs; Rahan computes historical averages, n_eff, errors, σ, and dropped-race logs at the Decision 012 horizons. Partisan-tagged polls stay preserved but are excluded from calibration.

## Active branch / commit

main at be97bf86c01e77b35514b5245e67635225a8a7d0, plus uncommitted source-proposal/plan documentation. `notebooks/data-pulls.ipynb` has pre-existing Rahan edits, preserved during this work.

## Data snapshot

Latest 2026 tracker: `data/raw/texas_tracker/20261006T023757Z/` — 18 tracker rows; source last updated October 3, 2026. Extraction is complete; primary verification is incomplete. Original `20260929T222648Z/` 16-row snapshot remains preserved.

Historical: `data/raw/texas_senate_historical/20261006T024116Z/` — 149 question/tracker records (262 older candidate rows plus 37 newer tracker rows). Source dates and populations preserved; one malformed 2024 date remains blank and flagged. Full primary verification and historical analytical inclusion remain pending.

The same historical snapshot also preserves the full 2018/2020 polling archive (4,593 candidate rows across all states); national derived preparation is not yet implemented. No election-results snapshot exists yet.

Prepared historical: `data/processed/texas_senate_historical/20261006T024116Z/` — 137 retained records, 12 exclusions, complete date/partisanship change audit. Original 149-row snapshot preserved. The one malformed 2024 fieldwork date remains blank and flagged; its election date is now populated.

## Blockers
