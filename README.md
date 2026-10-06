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

