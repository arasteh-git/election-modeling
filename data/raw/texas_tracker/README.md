# Texas Senate tracker snapshots

Snapshots of the [Texas 2026 U.S. Senate Poll Tracker](https://texaspolitics.utexas.edu/blog/texas-2026-u-s-senate-poll-tracker), Texas Politics Project at the University of Texas at Austin.

Each timestamped directory is a separate collection. The name is the collection time in UTC, not a poll publication date: `20260929T222648Z` means 2026-09-29 at 22:26:48 UTC. The first snapshot has 16 rows.

| File | Purpose |
| --- | --- |
| `source.html` | Original downloaded webpage, unchanged |
| `tracker.csv` | Source table cell text plus row IDs and release URLs; whitespace collapsed |
| `normalized.csv` | Same rows with consistent dates, column names, and numeric fields; no statistical normalization or poll selection |
| `manifest.json` | Source, attribution, collection timestamp, source update label, row count, transformations, and source-byte SHA-256 |
| `issues.json` | Automatic QC flags; neither corrections nor exclusions |

## Collect

From the repository root:

```bash
python src/ingest/texas_tracker.py
```

See the [collector instructions](../../../src/ingest/README.md) for offline replay.

## Limitations

- All CSV primary-verification statuses are pending. The [review notes](../../../docs/texas_tracker_review.md) cover the Emerson spot-check and the outstanding AARP discrepancy. Blank flags do not establish accuracy.
- Row IDs are local to a snapshot and may change across runs.

Keep source attribution with copies and preserve snapshots. See the [data dictionary](../../../docs/data_dictionary.md) and [source terms and provenance](../../../docs/data_sources.md).
