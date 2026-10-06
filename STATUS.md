# Project status

## Current milestone

Review the prepared historical Texas Senate polling inventory and choose the uncertainty model.

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

## Not yet done

- Local Python environment setup.
- Choice of error-model form, historical source/inclusion review, and approval of broader Senate polling and result sources for calibration.
- Open poll rule: LV numbers from releases where the tracker shows RV.
- Uncertainty model for win probability, and the baseline.
- Complete primary-source verification, analytical data cleaning, modeling, and evaluation.

## Next action

Rahan: load the prepared historical CSV, review remaining duplicate-question/field-date/source flags with Claude, decide remaining historical inclusion and availability rules, and choose the error-model form. Partisan polls are tagged and retained. Historical election results and a broader Senate calibration sample still need approved sources.

## Active branch / commit

main at bc15a9542c2470f22401a29743839c173e2092e4, plus uncommitted Decision 011 historical preparation and documentation changes.

## Data snapshot

data/raw/texas_tracker/20260929T222648Z/ — 16 tracker rows; source last updated September 23, 2026. Extraction is complete; primary verification is incomplete.

Historical: `data/raw/texas_senate_historical/20261006T024116Z/` — 149 question/tracker records (262 older candidate rows plus 37 newer tracker rows). Source dates and populations preserved; one malformed 2024 date remains blank and flagged. Full primary verification and historical analytical inclusion remain pending.

Prepared historical: `data/processed/texas_senate_historical/20261006T024116Z/` — 137 retained records, 12 exclusions, complete date/partisanship change audit. Original 149-row snapshot preserved. The one malformed 2024 fieldwork date remains blank and flagged; its election date is now populated.

## Blockers

