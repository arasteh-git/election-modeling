# Project status

## Current milestone

National calibration preparation implemented under Decisions 012–014. The saved contest/side/crosswalk snapshot has 729 selected questions, 873 exclusions and 348 pending questions. Rahan can begin margin/calibration work on eligible rounds while reviewing pending source, party and question-choice cases with Claude.

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

- Rahan approved MEDSL Senate V8.0/CC0 for 2018/2020/2024 (Decision 014). Collected immutable original CSV, pinned metadata, codebook and source listing with actual retrieval receipts/hashes. Mechanical inventory preserves 508 rows: 152/204/148 for requested years plus four Georgia 2021 runoff rows separately for review; full original CSV preserves 3,945 rows.
- Added `src/ingest/senate_results.py`, per-year inventories, 107 source-group coverage checks and exact row flags. Every source-group vote sum matches its reported total; 19 unofficial rows, 30 blank names, six noncandidate vote categories and repeated ballot lines remain retained. No result margins, poll/result crosswalks or model calculations performed.
- Six collector regression tests passed, including exact source-field preservation, year/round/special separation, anomaly retention, byte-identical offline replay, overwrite refusal, tamper rejection and schema/metadata/checksum validation. Source audit and notebook load paths are in `docs/senate_results_review.md` and the results/notebook READMEs.
- Final preservation check: all 33 existing polling/notebook files match the pre-collection SHA-256 baseline; notebook not edited/rerun. Collection handoff: `docs/handoffs/2026-10-06-codex-to-rahan-and-claude-results.md`.

- Chose normal errors for the minimum version; t-distribution to be tested in sensitivity analysis (Decision 015, 2026-10-06).

- Claude Code audited the MEDSL results snapshot (2026-10-06). Party labels conflict with Decision 013 sides (King, Sanders, Wyoming 2020); Mississippi 2018 has runoff returns only; some totals include noncandidate votes. A side mapping and crosswalk were requested from Codex (docs/handoffs/2026-10-06-claude-code-to-codex.md).

- Rahan authorized that handoff with “go” (2026-10-06). Implemented the offline preparer and explicit factual/alias JSON. Preserves all 508 result rows and 4,667 poll candidate answers, with 5,175 side mappings, 1,950 question crosswalks and 72 archive race mappings. No model calculations or notebook edits.
- The registry has 108 rounds: 74 in scope (56 eligible, two excluded, 16 pending), plus 34 outside-scope 2024 rounds. Maps Mississippi's 2018 special returns to November 27 runoff; registers the missing four-candidate November 6 first round as pending; maps Georgia January 2021 runoffs to cycle 2020; leaves Louisiana's unverified runoff unmapped.
- Selected factual references confirm King/Sanders/Ringelstein sides, Gross's Democratic nomination, Wyoming missing D/R labels, Maine first-choice counts and exceptional dates. Fusion ballot lines remain separate, 14 noncandidate rows are excluded from valid totals, and denominator ambiguity/unofficial returns/missing parties/reference disagreements remain pending. MEDSL counts are unchanged.
- Questions selected/excluded/pending: 2018 333/408/138; 2020 373/451/210; Texas 2024 23/14/0. Tied LV preferences and pending siblings stay pending. Selected questions cover 52 eligible rounds before horizon cutoffs.
- Nine preparation regression tests added; all 20 repository tests passed, including preservation, exact sides/rounds, valid votes, approved exclusions/preference, byte-identical replay, tamper rejection and overwrite refusal. All 47 pre-existing data files in the preservation baseline are unchanged. Rahan edited/committed the notebook during this task; Codex did not edit or execute it. See `docs/calibration_preparation_review.md` and the calibration handoff.

## Not yet done

- Local Python environment setup.
- Review the 16 pending in-scope contests and 348 pending questions. Missing Mississippi first-round returns need Rahan's supplemental-source/exclusion decision; Nevada denominator semantics, named blank-party candidates, unofficial returns, FEC disagreements, aliases and tied preferences remain unresolved. Exact keys/evidence are in the prepared logs and review.
- Comprehensive official-return/primary-poll verification. Checks so far are partial; source flags and mirror identity are not fully verified. Valid-vote categories and exceptional-round dates are prepared without changing MEDSL counts.
- Open poll rule: LV numbers from releases where the tracker shows RV.
- Rahan's side/margin function and horizon/calibration loop, including no-poll logs, counts, errors and RMSE. Normal errors are approved (Decision 015); calibrated sigma and sensitivity remain unimplemented.
- Complete primary-source verification, analytical data cleaning, modeling, and evaluation.

## Next action

Read `docs/calibration_preparation_review.md` and the prepared README. Rahan implements exact-round side sums/margins using valid votes, then horizon cutoffs, averages, n_eff, errors, RMSE, cycle means and dropped-race logs under Decision 012. Review pending cases with Claude and approve consequential resolutions before a fresh preparation snapshot.

## Active branch / commit

main at c3dc654 (observed during this task), plus uncommitted national preparer, reference JSON, processed snapshot, tests and documentation. Rahan committed notebook changes while Codex worked; Codex did not edit or execute it. No commit/push performed by Codex.

## Data snapshot

Latest 2026 tracker: `data/raw/texas_tracker/20261006T023757Z/` — 18 tracker rows; source last updated October 3, 2026. Extraction is complete; primary verification is incomplete. Original `20260929T222648Z/` 16-row snapshot remains preserved.

Historical: `data/raw/texas_senate_historical/20261006T024116Z/` — 149 question/tracker records (262 older candidate rows plus 37 newer tracker rows). Source dates and populations preserved; one malformed 2024 date remains blank and flagged. Full primary verification and historical analytical inclusion remain pending.

The same historical snapshot preserves the full 2018/2020 polling archive (4,593 candidate rows across all states); national preparation now uses that unchanged file.

Results: `data/raw/senate_results/20261006T035630Z/` — MEDSL V8.0/CC0 full original CSV (3,945 rows), supporting source files and receipts; 508 requested/supplemental rows, 107 source groups. Original CSV SHA-256 `6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd`. This is a source inventory, not a finalized calibration dataset. All prior polling raw/prepared snapshots remain unchanged.

Prepared historical: `data/processed/texas_senate_historical/20261006T024116Z/` — 137 retained records, 12 exclusions, complete date/partisanship change audit. Original 149-row snapshot preserved. The one malformed 2024 fieldwork date remains blank and flagged; its election date is now populated.

Prepared national calibration: `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1/` — 108 rounds, 508 candidate returns, 5,175 side mappings, 1,950 question crosswalks, audit logs and provenance/hashes. [README](data/processed/senate_calibration/README.md) gives offline replay/loading; no margins or core model code.

## Blockers
