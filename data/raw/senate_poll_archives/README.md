# Approved 2022/2024 Senate polling archives

Decision 017 approves the two dated FiveThirtyEight exports in [the proposal](../../../docs/polling_sources_2022_2024_proposal.md). **No complete polling snapshot is available yet:** collection attempts on 2026-10-08 failed to connect to Internet Archive. This folder currently contains documentation only. [Attempt receipts](../../../docs/senate_archive_collection_attempts_2026_10_08.json) and [the handoff](../../../docs/process/handoffs/2026-10-08-codex-to-rahan-and-claude-archive-collection.md) record the limit. No further source approval is needed to retry the same URLs.

From the repository root, standard library only:

```bash
python3 -B src/ingest/senate_poll_archives.py
```

A successful run creates a fresh UTC-stamped folder here; failed retrieval/validation writes no snapshot. Future snapshot files:

| File | Purpose |
| --- | --- |
| `senate_polls_2022_source.csv`, `senate_polls_2024_source.csv` | Complete unchanged original CSVs from the approved captures, including any other cycles in those source exports. |
| `publisher_README.md`, `publisher_polls_README.md` | Pinned publisher license and polling documentation. |
| `poll_candidate_rows.csv` | All designated-cycle candidate answers, original columns/strings plus source file, row, capture and question keys. |
| `poll_questions.csv` | One inventory row per source question, metadata, candidate-answer JSON and mechanical missing/inconsistency flags. No eligibility decision. |
| `race_inventory.csv` | Source race-ID coverage, dates/seats/stages as reported, question/poll-ID/LV counts. Not verified contest mappings. |
| `results_2022.csv`, `results_2022_coverage.csv` | Mechanical 2022 inventory/audit from the already-preserved MEDSL original. |
| `issues.json` | Poll-question and result flags, with counts; observations are retained. |
| `manifest.json` | Actual retrieval times, URLs, capture IDs, full-file hashes, publisher/license attribution, MEDSL provenance, counts, transformations and limits. |

After a successful collection, replay its exact source bytes without network:

```bash
python3 -B src/ingest/senate_poll_archives.py --snapshot data/raw/senate_poll_archives/ACTUAL_TIMESTAMP --output-root outputs/archive_replay
```

Replace `ACTUAL_TIMESTAMP` with an existing successful snapshot name. Existing outputs are never overwritten. Replay checks source receipts/hashes and reproduces the manifest and derived files byte for byte. Full-cycle counts/state coverage remain unknown until collection succeeds; tests use synthetic archive fixtures, not a real new polling dataset.

Polling attribution: FiveThirtyEight / ABC News, preserved by Internet Archive, CC BY 4.0 under the publisher dataset policy unless otherwise specified. Keep source/license links and identify derivatives. No linked poll-report redistribution permission is assumed. MEDSL V8.0 remains separately attributed/CC0. Current source selection does not change Texas 2024's active tracker inputs or implement margins, inclusion rules or forecasting.
