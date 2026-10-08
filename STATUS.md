# Project status

## Current milestone

Latest Texas forecast: P(Talarico wins) = 71.3% (2026-10-08 snapshot; first forecast 68.1%), Tier 1 minimum (Decision 010), with σ calibrated on 52 eligible 2018/2020/Texas 2024 contests (Decisions 012, 016). Next: sensitivity checks and automatic horizon selection.

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

- Rahan wrote the side-sum margins, poll/result merge and calibration loop in notebooks/data-pulls.ipynb (2026-10-07). 52 contests × 4 horizons: 197 errors, 11 dropped (Wyoming 2018/2020 at all horizons; DE/OR/WV 2020 at 42 days). Claude Code reproduced the run independently with identical results. h = 14:

  | Horizon | Races | Mean error | RMSE (σ) |
  | --- | ---: | ---: | ---: |
  | 7 | 50 | −2.84 | 6.50 |
  | 14 | 50 | −3.16 | 6.80 |
  | 28 | 50 | −3.87 | 7.03 |
  | 42 | 47 | −3.10 | 6.45 |

  Mean error by cycle: 2018 −0.1 to −1.8; 2020 −4.8 to −6.5. Provisional Texas check: Φ(3.32 / 7.03) ≈ 68% for the Democrat.
- Kept σ = RMSE with no bias shift (Decision 016).
- First Texas forecast (2026-10-08): P(Talarico wins) = 68.1%, from the `20261006T023757Z` snapshot average +3.32 (13 LV polls, h = 14, reference 2026-10-05) and σ = 7.03 (28-day horizon). Tier 1 deliverable (Decision 010) reached in its minimum form.
- Updated Texas forecast (2026-10-08): P(Talarico wins) = 71.3%, from the `20261008T042800Z` snapshot (one new LV poll, YouGov in-house D+6 ending 10-05): average +3.95, 14 LV polls, n_eff 6.71, h = 14, σ = 7.03 (28-day horizon). Claude Code reproduced the average and probability independently. The direct fetch failed from Rahan's network ("No route to host", though the page loads in a browser), so this snapshot was made from a browser-saved page with `--html` and `--retrieved-at`; its SHA-256 describes that saved copy.
- Requested a 2022/2024 all-state polling source proposal from Codex (docs/handoffs/2026-10-08-claude-code-to-codex.md); calibration scope unchanged until Rahan approves.
- Rahan authorized proposal research with “go do your work!” (2026-10-08). Codex verified public CSV headers and intended cycles in dated FiveThirtyEight archive prefixes, documented required fields and CC BY attribution, and proposed 2022/2024 expansion in `docs/polling_sources_2022_2024_proposal.md`. The unchanged local MEDSL original contains 168 source rows/36 groups for 2022 and 148/35 for 2024, both spanning 33 states; Georgia 2022 general/runoff returns are present. Full-cycle polling counts/coverage remain unmeasured. No complete new polling dataset, preparation, notebook execution or model calculation; sources/scope and MEDSL 2022 use remain pending approval.
- Rahan subsequently approved the two archives, all-state 2022/2024 scope and MEDSL 2022 use (Decision 017, 2026-10-08). Implemented `src/ingest/senate_poll_archives.py` with source/schema/license checks, immutable snapshots and verified offline replay. Actual archive connections failed; no complete new polling snapshot or expanded calibration inputs exist. Pinned GitHub documentation was reachable. Attempt receipts and the collection handoff record the limit.
- Inventoried 2022 results offline from the unchanged original: 168 rows, 36 separate source groups, 33 states; all group sums match reported totals. Missing detailed party fields on 13 source rows, two unofficial Missouri rows, ballot lines and vote categories remain retained. Files: `data/processed/senate_results_2022/20261006T035630Z_decision017_v1/`.
- Added approved mechanical wide exports for existing v1 inputs: `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1_wide/` provides 108 contest/round rows and 729 selected poll-question rows. Unknown votes/incomplete side counts and all contest statuses remain explicit. No margins or notebook changes by Codex. All 29 repository tests passed, including six synthetic-archive/results checks and three wide-export checks; real new polling coverage remains unverified.

## Not yet done

- Future expanded-model direction (Decision 018): use national and generic-ballot polls as lower-weight inputs to state predictions, adjusted for each state's partisan lean, alongside more states, pollster house effects and correlated state effects. Exact weights, lean/translation method, sources and validation remain undecided; no implementation added.

- Select the σ horizon automatically from the days remaining (currently set manually to 28).
- Sensitivity checks (h = 7/14/30, t with ν = 5 and 10, with/without thin races): planned for Rahan's next session.
- Thin races (deferred, 2026-10-08): 13–21 races per horizon have n_eff < 1.5; West Virginia 2020 (one poll, error −23) alone moves σ at 7 days from 6.50 to about 5.65. Rahan tentatively favors removing or blunting them, but will decide after the model runs on more states.
- Third/fourth calibration cycles: sources/scope and MEDSL 2022 use are approved. Awaiting successful archive retrieval, polling coverage inventory and extension of the preparer's schemas/round/date/side mappings. Independent sides, overlapping special-election questions and first-choice evidence still need review; the existing calibration sample has not expanded yet.

- Local Python environment setup.
- Review the 16 pending in-scope contests and 348 pending questions. Missing Mississippi first-round returns need Rahan's supplemental-source/exclusion decision; Nevada denominator semantics, named blank-party candidates, unofficial returns, FEC disagreements, aliases and tied preferences remain unresolved. Exact keys/evidence are in the prepared logs and review.
- Comprehensive official-return/primary-poll verification. Checks so far are partial; source flags and mirror identity are not fully verified. Valid-vote categories and exceptional-round dates are prepared without changing MEDSL counts.
- Open poll rule: LV numbers from releases where the tracker shows RV.
- Complete primary-source verification, analytical data cleaning, modeling, and evaluation.

## Next action

Retry `python3 -B src/ingest/senate_poll_archives.py` when public archive connectivity is restored; no new approval is needed for these pinned sources. Codex then inventories real polling coverage and extends preparation under existing rules. See [the handoff](docs/handoffs/2026-10-08-codex-to-rahan-and-claude-archive-collection.md). Rahan's modeling next steps remain sensitivity checks and automatic horizon selection.

## Active branch / commit

main; parent `bcee35b` before the documentation/roadmap commit requested by Rahan. Concurrent tracker/approval-tooling commits are preserved. The commit records completed workflow documentation and Decision 018; archive retrieval and expanded preparation remain outstanding.

## Data snapshot

Latest 2026 tracker: `data/raw/texas_tracker/20261008T042800Z/` — 19 tracker rows; source last updated October 6, 2026; saved from a browser and processed offline. Extraction is complete; primary verification is incomplete. Earlier `20260929T222648Z/` (16 rows) and `20261006T023757Z/` (18 rows) snapshots remain preserved.

Historical: `data/raw/texas_senate_historical/20261006T024116Z/` — 149 question/tracker records (262 older candidate rows plus 37 newer tracker rows). Source dates and populations preserved; one malformed 2024 date remains blank and flagged. Full primary verification and historical analytical inclusion remain pending.

The same historical snapshot preserves the full 2018/2020 polling archive (4,593 candidate rows across all states); national preparation now uses that unchanged file.

Results: `data/raw/senate_results/20261006T035630Z/` — MEDSL V8.0/CC0 full original CSV (3,945 rows), supporting source files and receipts; 508 requested/supplemental rows, 107 source groups. Original CSV SHA-256 `6f745db1b4a0026ad837e74428f9ed6f3f77fa51eb6f858b58ebdbc186fdb3bd`. This is a source inventory, not a finalized calibration dataset. All prior polling raw/prepared snapshots remain unchanged.

Prepared historical: `data/processed/texas_senate_historical/20261006T024116Z/` — 137 retained records, 12 exclusions, complete date/partisanship change audit. Original 149-row snapshot preserved. The one malformed 2024 fieldwork date remains blank and flagged; its election date is now populated.

Prepared national calibration: `data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1/` — 108 rounds, 508 candidate returns, 5,175 side mappings, 1,950 question crosswalks, audit logs and provenance/hashes. [README](data/processed/senate_calibration/README.md) gives offline replay/loading; no margins or core model code.

## Blockers

Approved Internet Archive downloads fail from this execution environment (connection/SSL timeout or “No route to host”). Pinned GitHub documentation succeeds; Browser fallback has no available browser connection. No complete new polling snapshot exists. This is a connectivity blocker, not a pending source-approval requirement.
