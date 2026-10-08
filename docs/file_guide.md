# Repository file guide

This guide describes the current files, not features that have already been implemented. Markdown (.md) is readable documentation; CSV is a spreadsheet-like table; JSON is structured metadata; .py is Python code; .ipynb is a notebook; HTML is a saved webpage.

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
| README.md | Project front door: scope, navigation, and commands. |
| PROJECT.md | Project agreement: roles, learning boundaries, scope, and decisions still needed. |
| STATUS.md | Current progress, blockers, next action, and data snapshot. |
| NEXT_STEPS.md | Ordered action checklist. |
| AGENTS.md | Codex instructions, including keeping core modeling work with Rahan. |
| CLAUDE.md | Claude's tutoring, auditing, debugging, and bias-review instructions. |
| .gitignore | Tells Git which untracked files to leave out, including local environments, credentials, and generated outputs. It does not remove files already tracked. |

## Shared documentation

| File | Purpose |
| --- | --- |
| docs/file_guide.md | This explanatory map of the repository. |
| docs/README.md | Shared-document navigation and the distinction between proposals, approved decisions, and implemented schemas/workflows. |
| docs/calibration_preparation_plan.md | Original national preparation design, approved source/rule updates and links to implemented behavior. |
| docs/calibration_preparation_review.md | Actual mapping/filter counts, official references, pending cases, preservation and observed tests. |
| docs/senate_results_review.md | Actual collected MEDSL V8.0 coverage, arithmetic/source flags, Texas source values, checks and remaining factual preparation work. |
| docs/data_dictionary.md | Meaning, types, units, identifiers, and missing-value conventions of the data fields. |
| docs/data_sources.md | Approved polling sources, proposed election-result sources, access methods, attribution, and snapshot provenance. |
| docs/decisions.md | History of decisions Rahan approved; later decisions can supersede earlier open questions. |
| docs/methodology.md | Home for approved statistical assumptions and formulas. Forecast target, scope, and first Texas poll rules are filled in (Decisions 008–009); blank sections are still undecided. |
| docs/texas_tracker_review.md | Human-readable source audit and outstanding issues; broader than the automatic issues.json. |
| docs/handoff_template.md | Blank structure for transferring a task between Rahan and assistants. |
| docs/handoffs/2026-09-27-claude-chat-to-claude-code.md | Historical onboarding and scaffold-audit handoff. |
| docs/handoffs/2026-09-29-codex-to-rahan-and-claude.md | Historical handoff for the Texas collection, checks, and unfinished verification. |
| docs/handoffs/2026-09-29-claude-code-to-codex.md | Decisions 008–010, Texas poll rules, first average check, and requested source proposal for Codex. |
| docs/handoffs/2026-10-05-claude-code-to-codex.md | Decision 012 calibration rules, audit of the 10-05 data, and requests for a results source and all-state 2018/2020 preparation. |
| docs/handoffs/2026-10-06-claude-code-to-codex.md | MEDSL results audit (party-label conflicts, Mississippi 2018 rounds, noncandidate totals) and request for contest, side-mapping, and poll crosswalk files. |
| docs/handoffs/2026-10-08-claude-code-to-codex.md | First calibration results (σ by horizon, cycle bias) and request for a 2022/2024 all-state polling source proposal. |
| docs/handoffs/2026-10-05-codex-to-rahan-and-claude-calibration-plan.md | Results-source research, corrected national archive counts, proposed preparation plan, observed checks, and decisions needed before collection. |
| docs/handoffs/2026-10-06-codex-to-rahan-and-claude-results.md | Approved-source collection, MEDSL snapshot/audit, preservation and six passing tests, current approved rules and remaining factual preparation work. |

## Python and notebooks

| File | Purpose |
| --- | --- |
| src/ingest/texas_tracker.py | Fetches the tracker and writes a new snapshot plus its CSVs, metadata, and issue log. Uses Python's standard library. Stops on certain unexpected formats; does not choose polls, weight them, or forecast. |
| notebooks/data-pulls.ipynb | Rahan's notebook. Installs/imports libraries, loads the 2026 Texas snapshot, and computes the recency-weighted LV average and effective poll count. |
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
| src/model/README.md | Placeholder guidance for Rahan's future modeling code. |
| src/evaluate/README.md | Placeholder guidance for Rahan's future forecast evaluation code. |
| outputs/README.md | Explains generated charts/results, which Git generally ignores. |
| tests/README.md | Commands and scope for the historical-preparation regression tests. |

## Empty directory markers

Each .gitkeep is an empty placeholder: Git tracks files rather than empty directories. There is no executable behavior. The existing markers are in data/raw/, data/processed/, notebooks/, outputs/, src/ingest/, src/clean/, src/model/, src/evaluate/, and tests/.

## Suggested reading order

Read the snapshot manifest, look at tracker.csv, compare normalized.csv, then read issues.json and docs/texas_tracker_review.md. Consult docs/data_dictionary.md while exploring in your notebook. Read methodology.md with Claude when ready to decide modeling rules.

## Historical Texas Senate files

`src/ingest/texas_senate_historical.py` collects and mechanically standardizes 2018/2020 archived FiveThirtyEight candidate data and UT's 2024 tracker. It preserves alternate questions and hypothetical candidates, flags issues, and supports offline replay. Run commands, output files, and limitations are in [data/raw/texas_senate_historical/README.md](../data/raw/texas_senate_historical/README.md).

First snapshot: `data/raw/texas_senate_historical/20261006T024116Z/`. It contains unchanged source CSV/HTML and publisher documentation, candidate-row/table extracts, combined `normalized.csv`, three per-cycle CSVs, `manifest.json`, and `issues.json`. It is an inventory for review, without historical inclusion decisions, weights, results, or uncertainty calibration.

[docs/handoffs/2026-10-05-codex-to-rahan-and-claude.md](handoffs/2026-10-05-codex-to-rahan-and-claude.md) records collection, observed checks, provenance limits, and next review steps.

## MEDSL Senate result files

`data/raw/senate_results/20261006T035630Z/` preserves unchanged `senate_returns.csv`, `metadata.json`, `codebook.md`, and `sources.csv`. `candidate_rows.csv` and `returns_2018.csv`/`returns_2020.csv`/`returns_2024.csv` preserve requested-year source strings; `returns_2021.csv` retains supplemental Georgia runoffs. `coverage.csv` checks source-group vote sums; `issues.json` lists flagged row IDs; `manifest.json` records receipts, source/output hashes, license, approval and limitations. No modeling margins or poll/result mappings are computed. [The results README](../data/raw/senate_results/README.md) explains every file and replay/loading; `tests/test_senate_results.py` checks preservation, group separation, anomalies, receipt integrity, byte-identical replay and overwrite protection. [The collection handoff](handoffs/2026-10-06-codex-to-rahan-and-claude-results.md) records observed work and remaining factual checks.

## Prepared historical Texas Senate files

`data/processed/texas_senate_historical/20261006T024116Z/` contains Decision 011 outputs. `normalized.csv` has 137 records with confirmed 2024 election dates and source-based partisan tags. The three per-cycle CSVs use the same schema. `excluded.csv` preserves the 12 removed hypothetical 2020 questions with reasons; `changes.csv` audits all 149 inputs; `manifest.json` records source provenance, hashes, rules, processing time, and counts. [The prepared README](../data/processed/texas_senate_historical/README.md) explains all files, reproduction, and the notebook load path.

`src/clean/prepare_texas_history.py` implements only the approved preparation rules. `tests/test_prepare_texas_history.py` checks exact exclusions, preserved values/inputs, date corrections, classifications, unknown/ambiguous cases, hashes, and overwrite protection. Run instructions are in their folder READMEs. [The cleanup handoff](handoffs/2026-10-05-codex-to-rahan-and-claude-history-cleanup.md) records this change and remaining review questions.

## Prepared national Senate calibration files

`src/clean/prepare_senate_calibration.py` is the offline, immutable preparer for Decisions 012–014. [src/clean/README.md](../src/clean/README.md) gives commands; [src/clean/calibration_references/README.md](../src/clean/calibration_references/README.md) explains `fec_facts.json`, `poll_aliases.json`, `round_facts.json` and the XLSX extractor `extract_fec.py`.

`data/processed/senate_calibration/20261006T024116Z_20261006T035630Z_v1/` contains `contests.csv`, `candidate_results.csv`, `candidate_side_map.csv`, `poll_candidate_rows.csv`, `poll_questions.csv`, `crosswalk.csv`, `race_crosswalk.csv`, `race_inventory.csv`, `excluded.csv`, `pending.csv`, `changes.csv` and `manifest.json`. [Its folder README](../data/processed/senate_calibration/README.md) describes each file, loading/replay commands, counts and limitations. No margins or calibration calculations are implemented. [The data dictionary](data_dictionary.md#prepared-national-calibration-inputs-decisions-012014) explains keys/fields/statuses.

`tests/test_prepare_senate_calibration.py` adds nine regression checks using the saved snapshots and temporary offline outputs. [The preparation review](calibration_preparation_review.md) and [handoff](handoffs/2026-10-06-codex-to-rahan-and-claude-calibration.md) record observed checks, source discrepancies, unconfirmed cases and Rahan's next steps. Downloaded official reference documents and implementation drafts remain under ignored `outputs/`; they are not additional tracked raw snapshots.
