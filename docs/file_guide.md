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

The normalized copy is stored beside the raw evidence for now because it is only a mechanical representation of that source. data/processed/ is reserved for future data produced under approved analytical rules.

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
| docs/data_dictionary.md | Meaning, types, units, identifiers, and missing-value conventions of the data fields. |
| docs/data_sources.md | Approved collection sources, access methods, attribution, and snapshot provenance. |
| docs/decisions.md | History of decisions Rahan approved; later decisions can supersede earlier open questions. |
| docs/methodology.md | Home for approved statistical assumptions and formulas. Currently an intentionally blank outline. |
| docs/texas_tracker_review.md | Human-readable source audit and outstanding issues; broader than the automatic issues.json. |
| docs/handoff_template.md | Blank structure for transferring a task between Rahan and assistants. |
| docs/handoffs/2026-09-27-claude-chat-to-claude-code.md | Historical onboarding and scaffold-audit handoff. |
| docs/handoffs/2026-09-29-codex-to-rahan-and-claude.md | Historical handoff for the Texas collection, checks, and unfinished verification. |

## Python and notebooks

| File | Purpose |
| --- | --- |
| src/ingest/texas_tracker.py | Fetches the tracker and writes a new snapshot plus its CSVs, metadata, and issue log. Uses Python's standard library. Stops on certain unexpected formats; does not choose polls, weight them, or forecast. |
| notebooks/data-pulls.ipynb | Rahan's notebook. Currently installs/imports matplotlib, plotnine, pandas, and NumPy and has an empty next cell. It does not yet load polls or implement a model. |

## Folder READMEs

| File | Purpose |
| --- | --- |
| data/raw/README.md | Explains original-source storage and links to the Texas collection. |
| data/raw/texas_tracker/README.md | Explains timestamped snapshots and all five generated files. |
| data/processed/README.md | Explains future analytically prepared datasets. None exist here yet. |
| notebooks/README.md | Explains the exploratory notebook and its current contents. |
| src/ingest/README.md | Collector instructions, outputs, offline replay, and limitations. |
| src/clean/README.md | Placeholder guidance for future cleaning scripts; none implemented here yet. |
| src/model/README.md | Placeholder guidance for Rahan's future modeling code. |
| src/evaluate/README.md | Placeholder guidance for Rahan's future forecast evaluation code. |
| outputs/README.md | Explains generated charts/results, which Git generally ignores. |
| tests/README.md | Home for future automated checks. No committed test suite currently exists. The extraction checks reported in the PR were run separately. |

## Empty directory markers

Each .gitkeep is an empty placeholder: Git tracks files rather than empty directories. There is no executable behavior. The existing markers are in data/raw/, data/processed/, notebooks/, outputs/, src/ingest/, src/clean/, src/model/, src/evaluate/, and tests/.

## Suggested reading order

Read the snapshot manifest, look at tracker.csv, compare normalized.csv, then read issues.json and docs/texas_tracker_review.md. Consult docs/data_dictionary.md while exploring in your notebook. Read methodology.md with Claude when ready to decide modeling rules.
