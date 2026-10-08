# Data pipeline

Collection and mechanical-preparation commands, moved here from the root README on 2026-10-08. Run each from the repository root. Collectors and preparers use only the Python standard library and write new timestamped snapshots. See [the file guide](file_guide.md) for every file and [data sources](data_sources.md) for provenance and permissions.

## Collection and preparation

Run `python src/ingest/texas_tracker.py` from the repository root (standard library only). See docs/data_sources.md for snapshots and docs/texas_tracker_review.md for outstanding verification.

Historical Texas Senate inventory (2018, 2020, 2024): run `python src/ingest/texas_senate_historical.py`. See [the inventory README](../data/raw/texas_senate_historical/README.md) for per-cycle CSVs, notebook loading, offline replay, source permissions, and review flags. First snapshot: `data/raw/texas_senate_historical/20261006T024116Z/`.

Prepare the historical inventory under Decision 011 with `python src/clean/prepare_texas_history.py`. [The prepared dataset](../data/processed/texas_senate_historical/README.md) contains 137 records with corrected 2024 election dates and source-based partisan tags, plus audits of 12 excluded hypothetical 2020 matchups. The README gives fresh-output replay commands and the notebook load path. Existing outputs are never overwritten; raw snapshots remain preserved.

Collect the approved MEDSL Senate results (Decision 014) with `python src/ingest/senate_results.py`. [The results README](../data/raw/senate_results/README.md) explains the pinned V8.0/CC0 source, 2018/2020/2024 inventories, separate Georgia 2021 runoff supplement, immutable snapshots, replay and notebook loading. First snapshot: `data/raw/senate_results/20261006T035630Z/`. [The review](senate_results_review.md) records source flags and coverage limits; no result margins or modeling denominator have been chosen by this collector.

[National calibration preparation](../data/processed/senate_calibration/README.md) is implemented under Decisions 012–014. Run `python3 -B src/clean/prepare_senate_calibration.py --output outputs/calibration_replay` for a fresh offline replay. The saved snapshot provides 108 contest rounds, 5,175 candidate mappings and 1,950 question crosswalks: 729 selected, 873 excluded and 348 pending. All sources remain preserved; dates, identities, denominator categories and approved filters are audited. [The review](calibration_preparation_review.md) lists pending source conflicts, missing returns, parties and question choices. Rahan implements margins and calibration. [The documentation README](README.md) explains the original plan, approved decisions, schemas and handoffs.

[The 2022/2024 polling sources](polling_sources_2022_2024_proposal.md) and scope expansion are approved under Decision 017. Run `python3 -B src/ingest/senate_poll_archives.py` when the archive is reachable; current connection failures have prevented a complete polling snapshot. [Collector documentation](../data/raw/senate_poll_archives/README.md) records files, replay and limits. The [2022 MEDSL inventory](../data/processed/senate_results_2022/README.md) is complete offline: 168 rows/36 groups. Expanded calibration preparation remains outstanding.

[Wide working tables](../data/processed/senate_calibration/README.md#wide-working-tables-existing-v1-inputs) now provide the existing v1 sample as 108 contest/round rows and 729 selected poll-question rows. Replay with `python3 -B src/clean/prepare_calibration_wide.py --output outputs/calibration_wide_replay`. Unknown votes remain explicit; these files compute no margins or model quantities.

## Repository layout

- `data/raw/`: original source inputs and their manifests; tracked in Git (Decision 005). `.gitattributes` keeps their bytes unchanged so manifest hashes match on every clone.
- `data/processed/`: derived inputs; tracked in Git (Decision 005).
- `src/ingest/` and `src/clean/`: collection and mechanical cleaning.
- `src/model/` and `src/evaluate/`: Rahan's model and calibration code.
- `notebooks/`: Rahan's working notebook.
- `tests/`: data-pipeline regression tests and model-refactor checks.
- `docs/`: methodology, data definitions, sources and decisions; `docs/process/` holds the collaboration agreement, checklists and handoffs.
