# 2026 Election Modeling

A personal learning project by Rahan Arasteh: use polling to forecast 2026 U.S. elections while developing Python, statistics, and modeling skills.

## File guide

See [the file-by-file guide](docs/file_guide.md) for every current file, including the five files inside each Texas polling snapshot.

## Start here

1. Read PROJECT.md for responsibilities and learning boundaries.
2. Read STATUS.md for the current state.
3. Follow NEXT_STEPS.md to set up the repository.
4. Record approved statistical choices in docs/methodology.md.

Blank sections are intentional: they represent decisions not yet made. Suggestions from earlier chats are not approved methodology.

## Repository URL
https://github.com/arasteh-git/election-modeling

## Election scope
Current focus: 2026 U.S. Senate races, starting with one race before expanding.
House modeling is deferred. Governor elections remain a possible longer-term extension.
First race: Texas Senate, using the Texas Politics Project tracker. Georgia and Michigan are tentative next races.

## Python version
Python 3.14.1

## Environment setup

## Data acquisition command

Run `python src/ingest/texas_tracker.py` from the repository root (standard library only). See docs/data_sources.md for snapshots and docs/texas_tracker_review.md for outstanding verification.

Historical Texas Senate inventory (2018, 2020, 2024): run `python src/ingest/texas_senate_historical.py`. See [the inventory README](data/raw/texas_senate_historical/README.md) for per-cycle CSVs, notebook loading, offline replay, source permissions, and review flags. First snapshot: `data/raw/texas_senate_historical/20261006T024116Z/`.

Prepare the historical inventory under Decision 011 with `python src/clean/prepare_texas_history.py`. [The prepared dataset](data/processed/texas_senate_historical/README.md) contains 137 records with corrected 2024 election dates and source-based partisan tags, plus audits of 12 excluded hypothetical 2020 matchups. The README gives fresh-output replay commands and the notebook load path. Existing outputs are never overwritten; raw snapshots remain preserved.

Collect the approved MEDSL Senate results (Decision 014) with `python src/ingest/senate_results.py`. [The results README](data/raw/senate_results/README.md) explains the pinned V8.0/CC0 source, 2018/2020/2024 inventories, separate Georgia 2021 runoff supplement, immutable snapshots, replay and notebook loading. First snapshot: `data/raw/senate_results/20261006T035630Z/`. [The review](docs/senate_results_review.md) records source flags and coverage limits; no result margins or modeling denominator have been chosen by this collector.

[National calibration preparation](data/processed/senate_calibration/README.md) is implemented under Decisions 012–014. Run `python3 -B src/clean/prepare_senate_calibration.py --output outputs/calibration_replay` for a fresh offline replay. The saved snapshot provides 108 contest rounds, 5,175 candidate mappings and 1,950 question crosswalks: 729 selected, 873 excluded and 348 pending. All sources remain preserved; dates, identities, denominator categories and approved filters are audited. [The review](docs/calibration_preparation_review.md) lists pending source conflicts, missing returns, parties and question choices. Rahan implements margins and calibration. [The documentation README](docs/README.md) explains the original plan, approved decisions, schemas and handoffs.

## Model execution command

## Evaluation command

## Structure

- docs/: methodology, data definitions, sources, decisions, and the handoff template.
- docs/handoffs/: dated handoff notes between assistants and Rahan (YYYY-MM-DD-from-to.md), based on docs/handoff_template.md.
- data/raw/: original source inputs; tracked in Git (Decision 005).
- data/processed/: derived inputs; tracked in Git (Decision 005).
- notebooks/: Rahan's exploration and learning work.
- src/ingest/ and src/clean/: collection and mechanical cleaning.
- src/model/ and src/evaluate/: Rahan's core modeling and evaluation code.
- tests/: future data validation and meaningful checks.

The 2026 tracker and historical Texas Senate inventory are available. Rahan's notebook implements the first recency-weighted LV average and effective poll count. The uncertainty model and scheduled automation remain unimplemented.
