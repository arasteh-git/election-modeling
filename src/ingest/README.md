# Data collection

## Files

- texas_tracker.py: collects the approved UT Texas Senate tracker and mechanically standardizes it. It uses only the Python standard library.
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
