# Data collection

Collectors that download approved sources into timestamped raw snapshots and standardize them mechanically. All use only the Python standard library, never overwrite an existing snapshot, and support offline replay from saved bytes. None applies inclusion rules, averaging, weighting, uncertainty or forecasts.

| File | Collects | Snapshot docs |
| --- | --- | --- |
| `texas_tracker.py` | The approved UT 2026 Texas Senate tracker | [data/raw/texas_tracker/](../../data/raw/texas_tracker/README.md) |
| `texas_senate_historical.py` | The 2018, 2020, and 2024 Texas Senate polling inventory | [data/raw/texas_senate_historical/](../../data/raw/texas_senate_historical/README.md) |
| `senate_results.py` | Pinned MEDSL V8.0 Senate results and a mechanical coverage audit (Decision 014) | [data/raw/senate_results/](../../data/raw/senate_results/README.md) |
| `senate_poll_archives.py` | Decision 017's pinned 2022/2024 archive captures, plus an inventory of the existing 2022 MEDSL results | [data/raw/senate_poll_archives/](../../data/raw/senate_poll_archives/README.md) |
| `.gitkeep` | Empty directory marker | |

Run all commands from the repository root.

## Texas tracker

```bash
python src/ingest/texas_tracker.py
```

Each run creates a new UTC-stamped folder under `data/raw/texas_tracker/` containing `source.html`, `tracker.csv`, `normalized.csv`, `manifest.json`, and `issues.json`.

Replay a saved page without the network:

```bash
python src/ingest/texas_tracker.py --html data/raw/texas_tracker/20260929T222648Z/source.html --retrieved-at 2026-09-29T22:26:48+00:00 --output-root outputs/texas_tracker_replay
```

Use the original retrieval time from `manifest.json`, not the time of replay. If the replay output already exists, choose a different `--output-root`. Replay files under `outputs/` are ignored by Git.

The collector checks the table header and row structure, parses 2026 fieldwork dates and numeric fields, and flags mismatched spreads, leaving original values intact. It does not verify every linked release or impute values. A source schema change can stop extraction and needs inspection. See the [review notes](../../docs/texas_tracker_review.md).

## Historical Texas Senate polling

```bash
python src/ingest/texas_senate_historical.py
python src/ingest/texas_senate_historical.py --snapshot data/raw/texas_senate_historical/20261006T024116Z --output-root outputs/history_replay
```

Uses the HTML parser from `texas_tracker.py`. Preserves original sources and candidate rows, exports a common schema and per-cycle CSVs, and flags unresolved dates, hypothetical matchups, and multiple questions from a poll. New snapshots go under `data/raw/texas_senate_historical/`. Offline replay verifies original hashes and keeps original retrieval times.

## MEDSL Senate results

```bash
python src/ingest/senate_results.py
python src/ingest/senate_results.py --snapshot data/raw/senate_results/20261006T035630Z --output-root outputs/senate_results_replay
```

Preserves the original CSV, metadata, codebook and source listing under `data/raw/senate_results/`, plus requested-year rows, separate Georgia 2021 runoff rows, coverage checks and flags. Offline replay verifies receipts and reproduces saved files. No dates, candidate mappings, denominators, margins or eligibility are inferred. `senate_results.audit` accepts an optional requested-year set and defaults to 2018/2020/2024.

## 2022/2024 Senate polling archives

```bash
python3 -B src/ingest/senate_poll_archives.py
python3 -B src/ingest/senate_poll_archives.py --results-only outputs/results_2022_replay
```

The first command needs public Internet Archive/GitHub access. It writes a new immutable timestamped snapshot only after all retrieval and validation succeeds. It preserves complete CSV bytes and publisher documentation, inventories designated-cycle candidate answers, questions and source races, and keeps missing or inconsistent values with flags. There is no side mapping, statistical calculation or primary-release verification. The second command is offline and reproduces the [168-row 2022 MEDSL inventory](../../data/processed/senate_results_2022/README.md).

Once a successful snapshot exists, replay it with `--snapshot PATH --output-root outputs/archive_replay`; original retrieval times and hashes are verified and preserved.

**Limitation:** archive connections currently fail, so no complete polling snapshot exists yet. Tests exercise replay with synthetic polling fixtures; they do not establish real 2022/2024 polling coverage.
