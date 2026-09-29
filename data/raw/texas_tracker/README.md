# Texas Senate tracker snapshots

Source: [Texas 2026 U.S. Senate Poll Tracker](https://texaspolitics.utexas.edu/blog/texas-2026-u-s-senate-poll-tracker), Texas Politics Project at the University of Texas at Austin.

Each timestamped directory is a separate collection. 20260929T222648Z means 2026-09-29 at 22:26:48 UTC, not a poll publication date.

| File | Purpose |
| --- | --- |
| source.html | Original downloaded webpage, unchanged |
| tracker.csv | Source table cell text plus row IDs and release URLs; whitespace collapsed |
| normalized.csv | Same rows with consistent dates, column names, and numeric fields; no statistical normalization or poll selection |
| manifest.json | Source, attribution, collection timestamp, source update label, row count, transformations, and source-byte SHA-256 |
| issues.json | Automatic QC flags; neither corrections nor exclusions |

The first snapshot has 16 rows. All CSV primary-verification statuses remain pending; consult [review notes](../../../docs/texas_tracker_review.md) for the Emerson spot-check and outstanding AARP discrepancy. Blank flags do not establish accuracy. Row IDs are local to a snapshot and may change across runs.

Run from repository root: `python src/ingest/texas_tracker.py`. Use [collector instructions](../../../src/ingest/README.md) for offline replay. Keep source attribution with copies and preserve snapshots. See [data dictionary](../../../docs/data_dictionary.md) and [source terms/provenance](../../../docs/data_sources.md).
