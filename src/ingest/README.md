# Data collection

## Files

- texas_tracker.py: collects the approved UT Texas Senate tracker and mechanically standardizes it. It uses only the Python standard library.
- senate_results.py: collects pinned MEDSL V8.0 Senate results and a mechanical coverage audit (Decision 014).
- senate_poll_archives.py: collects Decision 017's pinned 2022/2024 archive captures and inventories existing 2022 MEDSL results. Current archive connections fail; no complete new polling snapshot exists yet.
- .gitkeep: empty directory marker.

## Run from repository root

```bash
python src/ingest/texas_tracker.py
```

Each run creates a new UTC-stamped folder under data/raw/texas_tracker/ containing source.html, tracker.csv, normalized.csv, manifest.json, and issues.json. An existing folder is never overwritten.

## Replay a saved page without the network

```bash
python src/ingest/texas_tracker.py --html data/raw/texas_tracker/20260929T222648Z/source.html --retrieved-at 2026-09-29T22:26:48+00:00 --output-root outputs/texas_tracker_replay
```

Use the original retrieval time from manifest.json, not the time of replay. If replay output already exists, choose a different output-root. Generated replay files are ignored by Git under outputs/.

## Behavior and limits

Checks the table header and row structure, parses 2026 fieldwork dates and numeric fields, and flags mismatched spreads. Leaves original values intact. It does not verify every linked release, apply inclusion rules, impute values, or implement weighting or forecasts. A schema change can stop extraction and needs inspection.

See [snapshot file descriptions](../../data/raw/texas_tracker/README.md) and [review notes](../../docs/texas_tracker_review.md).

## MEDSL Senate results

```bash
python src/ingest/senate_results.py
python src/ingest/senate_results.py --snapshot data/raw/senate_results/20261006T035630Z --output-root outputs/senate_results_replay
```

Preserves original CSV/metadata/codebook/source listing under `data/raw/senate_results/`, plus requested-year rows, separate Georgia 2021 runoff rows, coverage checks and flags. Offline replay verifies receipts and reproduces saved files; existing outputs are never overwritten. Standard library only. See [snapshot files and limits](../../data/raw/senate_results/README.md). No dates, candidate mappings, denominators, margins or eligibility inferred.

## Approved 2022/2024 Senate archives

```bash
python3 -B src/ingest/senate_poll_archives.py
python3 -B src/ingest/senate_poll_archives.py --results-only outputs/results_2022_replay
```

Standard library only. The first command needs public Internet Archive/GitHub access; collection writes a new immutable timestamped snapshot only after all retrieval and validation succeeds. It preserves complete CSV bytes and publisher documentation, inventories designated-cycle candidate answers/questions/source races, and retains missing/inconsistent values with flags. No inclusion, side mapping, statistical calculations or primary-release verification. The second command is offline and reproduces the [168-row 2022 MEDSL inventory](../../data/processed/senate_results_2022/README.md).

After a real successful snapshot exists, replay with `--snapshot PATH --output-root outputs/archive_replay`; original retrieval times and hashes are verified and preserved. See [snapshot files and current connectivity limits](../../data/raw/senate_poll_archives/README.md). Tests exercise replay with synthetic polling fixtures; they do not establish real 2022/2024 polling coverage. Old MEDSL collection/replay remains unchanged; `senate_results.audit` now accepts an optional requested-year set without changing its original defaults.

## Historical Texas Senate collection

`texas_senate_historical.py` collects the requested 2018, 2020, and 2024 inventory, using only the standard library and the existing tracker HTML parser. It preserves original sources and candidate rows, exports a common schema and per-cycle CSVs, and flags unresolved dates, hypothetical matchups, and multiple questions from a poll.

```bash
python src/ingest/texas_senate_historical.py
python src/ingest/texas_senate_historical.py --snapshot data/raw/texas_senate_historical/20261006T024116Z --output-root outputs/history_replay
```

New timestamped snapshots go under `data/raw/texas_senate_historical/`; existing snapshots are never overwritten. Offline replay verifies original hashes and retains original retrieval times. See [historical source files, permissions, and limitations](../../data/raw/texas_senate_historical/README.md). No historical poll inclusion, averaging, uncertainty, or evaluation logic is implemented.
