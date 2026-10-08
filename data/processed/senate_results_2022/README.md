# 2022 MEDSL results inventory

A mechanical inventory of the 2022 rows in the preserved MEDSL V8.0 original, under Decision 017 (which extends the MEDSL V8.0 approval to 2022). The folder `20261006T035630Z_decision017_v1/` is named after the original retrieval, not a new network collection.

| File | Purpose |
| --- | --- |
| `returns_2022.csv` | All 168 original 2022 source rows/strings, source-row IDs, inventory-group IDs and flags. No candidate sides or election dates inferred. |
| `coverage.csv` | 36 source groups in 33 states, separating stage/special/mode; exact row-sum versus repeated-total checks. All differences are zero. |
| `issues.json` | Retained source flags and row IDs, including two unofficial Missouri rows, missing simplified parties and repeated ballot-line names. |
| `manifest.json` | Existing-source path, original retrieval receipt/SHA-256, V8.0/CC0 attribution, Decision 017, counts, transformations, output hashes and limits. |

The full original is in [the original MEDSL snapshot](../../raw/senate_results/README.md), where the original candidate strings and ballot lines stay available for audit.

## Load

Read with pandas `dtype=str, keep_default_na=False` to preserve original strings and empty fields. Georgia `GEN` and `GEN RUNOFF` are separate groups.

## Replay

Offline, to a fresh output directory:

```bash
python3 -B src/ingest/senate_poll_archives.py --results-only outputs/results_2022_replay
```

The collector verifies the original's SHA-256 and license/version. Generated files are deterministic, and existing outputs are never overwritten.

## Limitations

- Detailed parties are missing on 13 source rows in AK/HI/IL/IA/NV/NH/NC; blank fields are retained. The inherited audit flags simplified-party gaps separately. Detailed-party and first-choice verification still need preparation and review.
- Counts are uncorrected; no denominator or side rule is applied and no margins are calculated.
- This inventory alone cannot extend the calibration: 2022 polling and verified preparation are still required.
