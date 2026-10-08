# Repository file guide

This guide describes the current files, not features that have already been implemented. Markdown (.md) is readable documentation; CSV is a spreadsheet-like table; JSON is structured metadata; .py is Python code; .ipynb is a notebook; HTML is a saved webpage.

## Proposed 2022/2024 polling expansion

[polling_sources_2022_2024_proposal.md](polling_sources_2022_2024_proposal.md) records pinned URLs, field/license evidence, coverage limits and remaining preparation work. Approval is Decision 017. [polling_source_checks_2022_2024.json](polling_source_checks_2022_2024.json) contains initial metadata/header inspections; prefix hashes are not full new-dataset hashes. [senate_archive_collection_attempts_2026_10_08.json](senate_archive_collection_attempts_2026_10_08.json) records failed archive downloads and successful publisher-document checks. Full polling counts remain unmeasured.

`src/ingest/senate_poll_archives.py` is the approved collector, with offline replay and `--results-only` inventory mode. [Its README](../src/ingest/README.md) gives commands; [the raw-folder README](../data/raw/senate_poll_archives/README.md) describes future snapshot files. No real polling snapshot exists in that folder yet. [The current collection handoff](process/handoffs/2026-10-08-codex-to-rahan-and-claude-archive-collection.md) records the blocker and next action.

[2022 results inventory](../data/processed/senate_results_2022/README.md): `returns_2022.csv`, `coverage.csv`, `issues.json` and `manifest.json` preserve 168 original rows, 36 source groups and provenance. No side/date/denominator choices or model quantities.

[Wide current-v1 tables](../data/processed/senate_calibration/README.md#wide-working-tables-existing-v1-inputs): `results_wide.csv` (108 contest/round rows), `polls_wide.csv` (729 selected questions) and a parent/output hash manifest. `src/clean/prepare_calibration_wide.py` provides verified immutable export/replay; [the clean README](../src/clean/README.md) gives commands. These do not include new 2022/2024 polling. Unknown vote counts and result statuses are explicit; no margins are calculated.

[The Codex handoff](process/handoffs/2026-10-08-codex-to-rahan-and-claude-polling-sources.md) records completed proposal work and the approval required before collection. [handoffs/README.md](process/handoffs/README.md) indexes dated transfer notes and explains how to use the template.

## Start with the Texas snapshot

Folder: data/raw/texas_tracker/20260929T222648Z/. The name means September 29, 2026, at 22:26:48 UTC (6:26:48 p.m. New York). This is collection time, not the poll's publication or fieldwork date.

| File | What it is and when to use it |
| --- | --- |
| source.html | Original downloaded webpage, including the table. The evidence copy for checking extraction; leave unchanged. Opening locally may lack styling or require external assets. |
| tracker.csv | The 16 source table rows, with original cell text, row numbers, and release links. Whitespace is collapsed and relative links resolved. Use to compare with the source. |
| normalized.csv | The same 16 rows with consistent column names, full dates, numeric sample sizes and candidate shares, and QC flags. Use for initial Python exploration. “Normalized” means formatting standardized, not percentages rescaled, statistical normalization, or approved model input. |
| manifest.json | Collection receipt: source URL, attribution, retrieval time, source update label, row count, transformations, and SHA-256 fingerprint. The fingerprint detects changes to the original bytes; it does not establish factual accuracy. |
| issues.json | Machine-detected discrepancies. Currently flags AARP row 6: displayed shares imply D+5 but the tracker says D+4. A flag is not an automatic correction or exclusion. |

The 2026 normalized copy is stored beside the raw evidence because it is only a mechanical representation of that source. data/processed/ now also contains the historical Texas inventory prepared under Decision 011; see below.

Every verification status in the generated CSV remains pending. docs/texas_tracker_review.md records a narrower Emerson spot-check, the blocked AARP source, and remaining verification work.

## Root documents

| File | Purpose |
| --- | --- |
| README.md | Project front page: current forecast, method, calibration, how to run, limitations and roadmap. |
| STATUS.md | Current progress, blockers, next action, and data snapshot. |
| AGENTS.md | Codex instructions, including keeping core modeling work with Rahan. Stays at the root because Codex reads it from there. |
| CLAUDE.md | Claude's tutoring, auditing, debugging, and bias-review instructions. Stays at the root because Claude Code reads it from there. |
| requirements.txt | Pinned Python packages (pandas, NumPy, SciPy, matplotlib, plotnine, pytest) for Python 3.14. |
| pyproject.toml | pytest settings only: runs `tests/` with the repository root importable. |
| .gitattributes | Marks `data/raw/**` and `data/processed/**` as binary so Git never rewrites line endings; manifest SHA-256 hashes depend on the exact bytes. |
| .gitignore | Tells Git which untracked files to leave out, including local environments, credentials, and generated outputs. It does not remove files already tracked. |

PROJECT.md and NEXT_STEPS.md moved to [docs/process/](process/README.md) on 2026-10-08.

## Shared documentation

| File | Purpose |
| --- | --- |
| docs/file_guide.md | This explanatory map of the repository. |
| docs/data_pipeline.md | Collection and preparation commands and repository layout (moved from the root README). |
| docs/img/calibration_errors.png | Calibration chart embedded in the README; redraw with `python -m src.evaluate.plot_calibration`. |
| docs/process/README.md | Index of process documents: project agreement, setup checklist, handoffs. |
| docs/process/PROJECT.md | Project agreement: roles, learning boundaries, scope, and decisions still needed. |
| docs/process/NEXT_STEPS.md | Early setup checklist. |
| docs/README.md | Shared-document navigation and the distinction between proposals, approved decisions, and implemented schemas/workflows. |
| docs/calibration_preparation_plan.md | Original national preparation design, approved source/rule updates and links to implemented behavior. |
| docs/calibration_preparation_review.md | Actual mapping/filter counts, official references, pending cases, preservation and observed tests. |
| docs/senate_results_review.md | Actual collected MEDSL V8.0 coverage, arithmetic/source flags, Texas source values, checks and remaining factual preparation work. |
| docs/data_dictionary.md | Meaning, types, units, identifiers, and missing-value conventions of the data fields. |
| docs/data_sources.md | Approved polling sources, proposed election-result sources, access methods, attribution, and snapshot provenance. |
| docs/decisions.md | History of decisions Rahan approved; later decisions can supersede earlier open questions. |
| docs/methodology.md | Home for approved statistical assumptions and formulas. Blank sections are still undecided; the bias-shift sensitivity subsection is a TODO for Rahan. |
| docs/texas_tracker_review.md | Human-readable source audit and outstanding issues; broader than the automatic issues.json. |
| docs/handoff_template.md | Blank structure for transferring a task between Rahan and assistants. |
| docs/process/handoffs/2026-10-08-claude-code-to-rahan-portfolio-cleanup.md | Portfolio cleanup: fresh-clone hash fix, `src/` refactor, README rewrite and docs reorganization, with checks and open items. |
| docs/process/handoffs/2026-09-27-claude-chat-to-claude-code.md | Historical onboarding and scaffold-audit handoff. |
| docs/process/handoffs/2026-09-29-codex-to-rahan-and-claude.md | Historical handoff for the Texas collection, checks, and unfinished verification. |
| docs/process/handoffs/2026-09-29-claude-code-to-codex.md | Decisions 008–010, Texas poll rules, first average check, and requested source proposal for Codex. |
| docs/process/handoffs/2026-10-05-claude-code-to-codex.md | Decision 012 calibration rules, audit of the 10-05 data, and requests for a results source and all-state 2018/2020 preparation. |
| docs/process/handoffs/2026-10-06-claude-code-to-codex.md | MEDSL results audit (party-label conflicts, Mississippi 2018 rounds, noncandidate totals) and request for contest, side-mapping, and poll crosswalk files. |
| docs/process/handoffs/2026-10-08-claude-code-to-codex.md | First calibration results (σ by horizon, cycle bias) and request for a 2022/2024 all-state polling source proposal. |
| docs/process/handoffs/2026-10-05-codex-to-rahan-and-claude-calibration-plan.md | Results-source research, corrected national archive counts, proposed preparation plan, observed checks, and decisions needed before collection. |
| docs/process/handoffs/2026-10-06-codex-to-rahan-and-claude-results.md | Approved-source collection, MEDSL snapshot/audit, preservation and six passing tests, current approved rules and remaining factual preparation work. |

## Python and notebooks

| File | Purpose |
| --- | --- |
| src/ingest/texas_tracker.py | Fetches the tracker and writes a new snapshot plus its CSVs, metadata, and issue log. Uses Python's standard library. Stops on certain unexpected formats; does not choose polls, weight them, or forecast. |
| notebooks/texas_forecast.ipynb | Rahan's notebook (formerly data-pulls.ipynb). Imports the model/calibration functions from `src/` and walks through the Texas average, calibration and win probability. |
| src/model/polling_average.py | Margin helpers and `weighted_avg` (recency-weighted average and n_eff). |
| src/model/win_probability.py | `p_dem_win`: Φ(average / σ). |
| src/model/run_texas.py | Reproduces the current Texas forecast: `python -m src.model.run_texas`. |
| src/evaluate/calibration.py | Historical results/polls tables, calibration loop, and mean error/RMSE summaries. |
| src/evaluate/plot_calibration.py | Draws docs/img/calibration_errors.png. |
| tests/test_texas_model.py | Checks that the `src/` code reproduces the notebook's saved results exactly. |
| src/clean/prepare_texas_history.py | Applies approved historical date corrections, source-based partisan tags, and the 12 hypothetical-matchup exclusions, preserving raw snapshots and audit files. |
| src/ingest/senate_results.py | Collects the approved pinned MEDSL results; preserves original sources and per-year rows, flags issues and audits source-group totals; supports immutable offline replay. |

## Folder READMEs

| File | Purpose |
| --- | --- |
| data/raw/README.md | Explains original-source storage and links to the Texas collection. |
| data/raw/senate_results/README.md | MEDSL attribution/CC0, collection and replay commands, all 12 snapshot files, source-year counts, notebook loading and preparation limits. |
| data/raw/texas_tracker/README.md | Explains timestamped snapshots and all five generated files. |
| data/processed/README.md | Explains derived data and links to the prepared historical Texas inventory. |
| data/processed/texas_senate_historical/README.md | Prepared historical files, classifications, audits, reproduction commands, and notebook load path. |
| notebooks/README.md | Explains the exploratory notebook and its current contents. |
| src/ingest/README.md | Collector instructions, outputs, offline replay, and limitations. |
| src/clean/README.md | Historical preparation commands, outputs, and limits under Decision 011. |
| src/model/README.md | Rahan's model code: files and the run command. |
| src/evaluate/README.md | Rahan's calibration code and the chart script. |
| outputs/README.md | Explains generated charts/results, which Git generally ignores. |
| tests/README.md | Commands and scope for all 34 tests. |

## Empty directory markers

Each .gitkeep is an empty placeholder (`src/__init__.py`, `src/model/__init__.py` and `src/evaluate/__init__.py` are likewise empty; they make `src.model` importable): Git tracks files rather than empty directories. There is no executable behavior. The existing markers are in data/raw/, data/processed/, notebooks/, outputs/, src/ingest/, src/clean/, src/model/, src/evaluate/, and tests/.

## Suggested reading order

Read the snapshot manifest, look at tracker.csv, compare normalized.csv, then read issues.json and docs/texas_tracker_review.md. Consult docs/data_dictionary.md while exploring in your notebook. Read methodology.md with Claude when ready to decide modeling rules.

## Historical Texas Senate files

`src/ingest/texas_senate_historical.py` collects and mechanically standardizes 2018/2020 archived FiveThirtyEight candidate data and UT's 2024 tracker. It preserves alternate questions and hypothetical candidates, flags issues, and supports offline replay. Run commands, output files, and limitations are in [data/raw/texas_senate_historical/README.md](../data/raw/texas_senate_historical/README.md).

First snapshot: `data/raw/texas_senate_historical/20261006T024116Z/`. It contains unchanged source CSV/HTML and publisher documentation, candidate-row/table extracts, combined `normalized.csv`, three per-cycle CSVs, `manifest.json`, and `issues.json`. It is an inventory for review, without historical inclusion decisions, weights, results, or uncertainty calibration.

[docs/handoffs/2026-10-05-codex-to-rahan-and-claude.md](process/handoffs/2026-10-05-codex-to-rahan-and-claude.md) records collection, observed checks, provenance limits, and next review steps.

## MEDSL Senate result files

`data/raw/senate_results/20261006T035630Z/` preserves unchanged `senate_returns.csv`, `metadata.json`, `codebook.md`, and `sources.csv`. `candidate_rows.csv` and `returns_2018.csv`/`returns_2020.csv`/`returns_2024.csv` preserve requested-year source strings; `returns_2021.csv` retains supplemental Georgia runoffs. `coverage.csv` checks source-group vote sums; `issues.json` lists flagged row IDs; `manifest.json` records receipts, source/output hashes, license, approval and limitations. No modeling margins or poll/result mappings are computed. [The results README](../data/raw/senate_results/README.md) explains every file and replay/loading; `tests/test_senate_results.py` checks preservation, group separation, anomalies, receipt integrity, byte-identical replay and overwrite protection. [The collection handoff](process/handoffs/2026-10-06-codex-to-rahan-and-claude-results.md) records observed work and remaining factual checks.

## Prepared historical Texas Senate files

`data/processed/texas_senate_historical/20261006T024116Z/` contains Decision 011 outputs. `normalized.csv` has 137 records with confirmed 2024 election dates and source-based partisan tags. The three per-cycle CSVs use the same schema. `excluded.csv` preserves the 12 removed hypothetical 2020 questions with reasons; `changes.csv` audits all 149 inputs; `manifest.json` records source provenance, hashes, rules, processing time, and counts. [The prepared README](../data/processed/texas_senate_historical/README.md) explains all files, reproduction, and the notebook load path.

`src/clean/prepare_texas_history.py` implements only the approved preparation rules. `tests/test_prepare_texas_history.py` checks exact exclusions, preserved values/inputs, date corrections, classifications, unknown/ambiguous cases, hashes, and overwrite protection. Run instructions are in their folder READMEs. [The cleanup handoff](process/handoffs/2026-10-05-codex-to-rahan-and-claude-history-cleanup.md) records this change and remaining review questions.

## Prepared national Senate calibration files

`src/clean/prepare_senate_calibration.py` is the offline, immutable preparer for Decisions 012–014. [src/clean/README.md](../src/clean/README.md) gives commands; [src/clean/calibration_references/README.md](../src/clean/calibration_references/README.md) explains `fec_facts.json`, `poll_aliases.json`, `round_facts.json` and the XLSX extractor `extract_fec.py`.

`data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1/` contains `contests.csv`, `candidate_results.csv`, `candidate_side_map.csv`, `poll_candidate_rows.csv`, `poll_questions.csv`, `crosswalk.csv`, `race_crosswalk.csv`, `race_inventory.csv`, `excluded.csv`, `pending.csv`, `changes.csv` and `manifest.json`. [Its folder README](../data/processed/senate_calibration/README.md) describes each file, loading/replay commands, counts and limitations. No margins or calibration calculations are implemented. [The data dictionary](data_dictionary.md#prepared-national-calibration-inputs-decisions-012014) explains keys/fields/statuses.

`tests/test_prepare_senate_calibration.py` adds nine regression checks using the saved snapshots and temporary offline outputs. [The preparation review](calibration_preparation_review.md) and [handoff](process/handoffs/2026-10-06-codex-to-rahan-and-claude-calibration.md) record observed checks, source discrepancies, unconfirmed cases and Rahan's next steps. Downloaded official reference documents and implementation drafts remain under ignored `outputs/`; they are not additional tracked raw snapshots.
